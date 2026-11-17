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


def tool_results_text(lines):
    out = []
    for line in lines:
        if line.get("type") != "user":
            continue
        content = line.get("message", {}).get("content", [])
        for block in content if isinstance(content, list) else []:
            if block.get("type") == "tool_result":
                inner = block.get("content")
                if isinstance(inner, list):
                    inner = "\n".join(b.get("text", "") for b in inner if isinstance(b, dict))
                out.append(inner or "")
    return "\n".join(out)


def facts(lines):
    files = index_files()
    final = next((l.get("result", "") for l in reversed(lines) if l.get("type") == "result"), "")
    uses = list(tool_uses(lines))
    main_reads = [b["input"].get("file_path") or b["input"].get("path") or "" for parent, b in uses
                  if parent is None and b["name"] in ("Read", "Grep")]
    trace = final.rsplit("Knowledge trace", 1)[1] if "Knowledge trace" in final else ""
    trace = re.split(r"Auditor verdict|Reviewer score|## QA pending", trace)[0]
    cited = sorted(set(ID.findall(trace)))
    everything = final + "\n" + tool_results_text(lines)
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
        "unread_ids": [i for i in cited if i in files
                       and not any(p.endswith("knowledge/" + files[i]) for p in main_reads)],
        "index_read_whole": any(b["name"] == "Read" and b["input"].get("file_path", "").endswith("knowledge/index.md")
                                and not b["input"].get("limit") for _, b in uses),
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
    # A Grep on the entry's file counts as reading it; the contract text "PASS|FAIL" is not a verdict.
    lines[1]["message"]["content"][0] = {"type": "tool_use", "id": "b", "name": "Grep",
                                         "input": {"pattern": "^## F224", "path": f"/x/knowledge/{files[real]}"}}
    lines.insert(0, {"type": "user", "message": {"content": [
        {"type": "tool_result", "content": "Auditor verdict: PASS|FAIL"}]}})
    out = facts(lines)
    assert out["unread_ids"] == [], out["unread_ids"]
    assert out["auditor_verdicts"] == ["FAIL"], out["auditor_verdicts"]
    lines[3]["message"]["content"][0]["input"].pop("limit")
    assert facts(lines)["index_read_whole"] is True
    print("selftest OK")


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        demo()
    else:
        with open(sys.argv[1]) as fh:
            parsed = [json.loads(line) for line in fh if line.strip().startswith("{")]
        print(json.dumps(facts(parsed), indent=2, ensure_ascii=False))
