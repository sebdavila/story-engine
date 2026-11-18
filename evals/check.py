"""Mechanical facts from a `claude -p --output-format stream-json --verbose` transcript.

Usage: python3 evals/check.py <transcript.jsonl>   prints facts as JSON
       python3 evals/check.py --selftest
"""
import json
import re
import sys
from pathlib import Path

KNOWLEDGE = Path(__file__).resolve().parent.parent / "knowledge"
ID = re.compile(r"\b[FST]\d{3}\b")


def index_files():
    rows = re.findall(r"^\| ([FST]\d{3}) \| .*? \| (\S+) \|$", (KNOWLEDGE / "index.md").read_text(), re.M)
    return dict(rows)


def tool_uses(lines):
    for line in lines:
        if line.get("type") != "assistant":
            continue
        for block in line["message"].get("content", []):
            if block.get("type") == "tool_use":
                yield line.get("parent_tool_use_id"), block


def tool_results_text(lines, main_only=False):
    out = []
    for line in lines:
        if line.get("type") != "user" or (main_only and line.get("parent_tool_use_id")):
            continue
        content = line.get("message", {}).get("content", [])
        for block in content if isinstance(content, list) else []:
            if block.get("type") == "tool_result":
                inner = block.get("content")
                if isinstance(inner, list):
                    inner = "\n".join(b.get("text", "") for b in inner if isinstance(b, dict))
                out.append(inner or "")
    return "\n".join(out)


INDEX_LINES = len((KNOWLEDGE / "index.md").read_text().splitlines())


def reads_index_whole(b):
    inp = b["input"]
    path = inp.get("file_path") or inp.get("path") or ""
    if not path.endswith("knowledge/index.md"):
        return False
    if b["name"] == "Read":
        return not inp.get("limit") or inp["limit"] >= INDEX_LINES
    if b["name"] == "Grep":
        try:
            return re.search(inp.get("pattern", ""), "") is not None
        except re.error:
            return False
    return False


def facts(lines):
    files = index_files()
    final = next((l.get("result", "") for l in reversed(lines) if l.get("type") == "result"), "")
    uses = list(tool_uses(lines))
    main_reads = [b["input"].get("file_path", "") for parent, b in uses if parent is None and b["name"] == "Read"]

    main_results = tool_results_text(lines, main_only=True)

    def was_read(i):
        if re.search(rf"(## |\*\*){i} ·", main_results):
            return True
        # A Grep counts only through the heading check above; a Read counts by its path.
        return any(path.endswith("knowledge/" + files[i]) for path in main_reads)
    trace = final.rsplit("Knowledge trace", 1)[1] if "Knowledge trace" in final else ""
    trace = re.split(r"Auditor verdict|Reviewer score|## QA pending", trace)[0]
    cited = sorted(set(ID.findall(trace)))
    everything = tool_results_text(lines) + "\n" + final
    verdicts = re.findall(r"Auditor verdict:\**\s*(PASS|FAIL)(?!\|)", everything)
    scores = [int(s) for s in re.findall(r"Reviewer score:\**\s*(\d+)\s*/\s*20", everything)]
    final_verdict = re.findall(r"Auditor verdict:\**\s*(PASS|FAIL)(?!\|)", final)
    final_score = re.findall(r"Reviewer score:\**\s*(\d+)\s*/\s*20", final)
    return {
        "skills": [b["input"].get("skill") for _, b in uses if b["name"] == "Skill"],
        "agents": [b["input"].get("subagent_type") for _, b in uses if b["name"] in ("Agent", "Task")],
        "trace_present": "Knowledge trace" in final,
        "cited_ids": cited,
        "missing_ids": [i for i in cited if i not in files],
        "unread_ids": [i for i in cited if i in files and not was_read(i)],
        "index_read_whole": any(reads_index_whole(b) for _, b in uses),
        "auditor_verdicts": verdicts,
        "reviewer_scores": scores,
        "auditor_verdict": final_verdict[-1] if final_verdict else (verdicts[-1] if verdicts else None),
        "reviewer_score": int(final_score[-1]) if final_score else (scores[-1] if scores else None),
        "final_text": final,
    }


def demo():
    files = index_files()
    real = "F224"
    lines = [
        {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
            {"type": "tool_use", "id": "a", "name": "Skill", "input": {"skill": "story-engine:story-structure"}}]}},
        {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
            {"type": "tool_use", "id": "b", "name": "Read",
             "input": {"file_path": f"/x/knowledge/{files[real]}"}}]}},
        {"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
            {"type": "tool_use", "id": "c", "name": "Read",
             "input": {"file_path": "/x/knowledge/index.md", "limit": 20}}]}},
        {"type": "result", "result": f"Beats...\nKnowledge trace\n- Read: x\n- Framework: A ({files[real]} {real}) -> 1\n- Techniques: B (F999) -> 2\n\nAuditor verdict: FAIL\nReviewer score: 12/20"},
    ]
    out = facts(lines)
    assert out["skills"] == ["story-engine:story-structure"], out["skills"]
    assert out["missing_ids"] == ["F999"], out["missing_ids"]
    assert out["unread_ids"] == [], out["unread_ids"]
    assert out["index_read_whole"] is False
    assert out["trace_present"] is True
    assert out["auditor_verdict"] == "FAIL"
    assert out["reviewer_score"] == 12
    # A Grep counts only when its result shows the entry heading; "PASS|FAIL" is not a verdict.
    lines[1]["message"]["content"][0] = {"type": "tool_use", "id": "b", "name": "Grep",
                                         "input": {"pattern": "^## F224", "path": "/x/knowledge"}}
    lines.insert(0, {"type": "user", "message": {"content": [
        {"type": "tool_result", "content": "Auditor verdict: PASS|FAIL"}]}})
    out = facts(lines)
    assert out["unread_ids"] == ["F224"], out["unread_ids"]
    assert out["auditor_verdicts"] == ["FAIL"], out["auditor_verdicts"]
    lines.insert(0, {"type": "user", "message": {"content": [
        {"type": "tool_result", "content": "frameworks/x.md:65:## F224 · Something\nAuditor verdict: PASS"}]}})
    out = facts(lines)
    assert out["unread_ids"] == [], out["unread_ids"]
    assert out["auditor_verdicts"] == ["PASS", "FAIL"], out["auditor_verdicts"]
    # Whole index: a Read without a small limit, or a Grep whose pattern matches every line.
    index_read = lines[4]["message"]["content"][0]
    index_read["input"]["limit"] = 2000
    assert facts(lines)["index_read_whole"] is True
    lines[4]["message"]["content"][0] = {"type": "tool_use", "id": "c", "name": "Grep",
                                         "input": {"pattern": r"\| F224 \|", "path": "/x/knowledge/index.md"}}
    assert facts(lines)["index_read_whole"] is False
    lines[4]["message"]["content"][0]["input"]["pattern"] = "| F224 |"
    assert facts(lines)["index_read_whole"] is True
    print("selftest OK")


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        demo()
    else:
        with open(sys.argv[1]) as fh:
            parsed = [json.loads(line) for line in fh if line.strip().startswith("{")]
        print(json.dumps(facts(parsed), indent=2, ensure_ascii=False))
