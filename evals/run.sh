#!/bin/bash
# Run eval cases against the working copy of the plugin.
# Usage: bash evals/run.sh <round> [id ...]   (no ids = all cases; at most 3 run at once)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ROUND="$1"; shift
OUT="$REPO/../story-engine-workspace/round-$ROUND"
IDS="${*:-$(python3 -c "import json;print(' '.join(str(e['id']) for e in json.load(open('$REPO/evals/evals.json'))['evals']))")}"

run_case() {
  local id="$1" dir="$OUT/case-$1"
  mkdir -p "$dir"
  python3 - "$REPO" "$id" "$dir" <<'PY'
import json, shutil, sys
repo, cid, d = sys.argv[1], int(sys.argv[2]), sys.argv[3]
case = next(e for e in json.load(open(f"{repo}/evals/evals.json"))["evals"] if e["id"] == cid)
for f in case["files"]:
    shutil.copy(f"{repo}/evals/files/{f}", d)
open(f"{d}/prompt.txt", "w").write(case["prompt"])
PY
  (cd "$dir" && claude -p "$(cat prompt.txt)" --plugin-dir "$REPO" --output-format stream-json --verbose \
      --allowedTools "Read,Grep,Glob,Skill,Agent" < /dev/null > transcript.jsonl 2> stderr.txt) || true
  python3 "$REPO/evals/check.py" "$dir/transcript.jsonl" > "$dir/facts.json"
  echo "case $id done"
}
export -f run_case; export REPO OUT
echo $IDS | tr ' ' '\n' | xargs -P 3 -I{} bash -c 'run_case {}'
