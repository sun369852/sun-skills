#!/usr/bin/env python3
"""Windows-compatible trigger eval runner for manual use.

This helper calls the local `claude` CLI and sends eval queries to the model
provider. Run it only when that external data transfer is acceptable.

The package script skips `evals/`, so this helper is intentionally kept out of
the distributable `.skill` file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple[str, str]:
    content = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md frontmatter not found")
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match or not desc_match:
        raise ValueError("SKILL.md must contain name and description")
    return name_match.group(1).strip(), desc_match.group(1).strip()


def find_project_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".claude").is_dir():
            return candidate
    return start


def output_mentions_skill(output: str, clean_name: str) -> bool:
    pending_tool_name = None
    accumulated_json = ""
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if event.get("type") == "stream_event":
            stream_event = event.get("event", {})
            stream_type = stream_event.get("type", "")

            if stream_type == "content_block_start":
                content_block = stream_event.get("content_block", {})
                if content_block.get("type") == "tool_use":
                    tool_name = content_block.get("name", "")
                    if tool_name in ("Skill", "Read"):
                        pending_tool_name = tool_name
                        accumulated_json = ""
                    else:
                        pending_tool_name = None
                        accumulated_json = ""

            elif stream_type == "content_block_delta" and pending_tool_name:
                delta = stream_event.get("delta", {})
                if delta.get("type") == "input_json_delta":
                    accumulated_json += delta.get("partial_json", "")
                    if clean_name in accumulated_json:
                        return True

            elif stream_type == "content_block_stop":
                if pending_tool_name and clean_name in accumulated_json:
                    return True
                pending_tool_name = None
                accumulated_json = ""

        elif event.get("type") == "assistant":
            message = event.get("message", {})
            for content_item in message.get("content", []):
                if content_item.get("type") != "tool_use":
                    continue
                tool_name = content_item.get("name", "")
                tool_input = content_item.get("input", {})
                if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                    return True
                if tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                    return True
    return False


def run_query(query: str, skill_name: str, description: str, project_root: Path, model: str, timeout: int) -> dict:
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    commands_dir = project_root / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"
    commands_dir.mkdir(parents=True, exist_ok=True)

    indented_desc = "\n  ".join(description.splitlines())
    command_file.write_text(
        "---\n"
        "description: |\n"
        f"  {indented_desc}\n"
        "---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {description}\n",
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        started_at = time.time()
        completed = subprocess.run(
            [
                "claude",
                "-p",
                query,
                "--output-format",
                "stream-json",
                "--verbose",
                "--include-partial-messages",
                "--model",
                model,
            ],
            cwd=project_root,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
        )
        combined = (completed.stdout or "") + "\n" + (completed.stderr or "")
        return {
            "triggered": output_mentions_skill(combined, clean_name),
            "timed_out": False,
            "duration_seconds": round(time.time() - started_at, 3),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "triggered": output_mentions_skill(stdout + "\n" + stderr, clean_name),
            "timed_out": True,
            "duration_seconds": timeout,
        }
    finally:
        try:
            command_file.unlink()
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-set", required=True)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--runs-per-query", type=int, default=1)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_name, description = parse_skill_md(Path(args.skill_path))
    project_root = find_project_root(Path.cwd())
    results = []
    passed = 0
    for idx, item in enumerate(eval_set, 1):
        runs = []
        for run_idx in range(1, args.runs_per_query + 1):
            run_result = run_query(item["query"], skill_name, description, project_root, args.model, args.timeout)
            runs.append({"run": run_idx, **run_result})
            print(
                f"run {run_idx}/{args.runs_per_query} triggered={run_result['triggered']} "
                f"timeout={run_result['timed_out']} :: {item['query'][:70]}"
            )
            sys.stdout.flush()
        trigger_count = sum(1 for run in runs if run["triggered"])
        trigger_rate = trigger_count / args.runs_per_query
        triggered = trigger_rate >= args.trigger_threshold
        ok = triggered == item["should_trigger"]
        passed += int(ok)
        results.append({
            **item,
            "id": idx,
            "runs": runs,
            "trigger_count": trigger_count,
            "runs_per_query": args.runs_per_query,
            "trigger_rate": trigger_rate,
            "triggered": triggered,
            "passed": ok,
        })
        print(
            f"{'PASS' if ok else 'FAIL'} trigger_rate={trigger_rate:.2f} "
            f"triggered={triggered} expected={item['should_trigger']} {item['query'][:80]}"
        )
        sys.stdout.flush()

    summary = {
        "skill_name": skill_name,
        "model": args.model,
        "timeout_seconds": args.timeout,
        "runs_per_query": args.runs_per_query,
        "trigger_threshold": args.trigger_threshold,
        "passed": passed,
        "total": len(results),
        "accuracy": passed / len(results) if results else 0,
        "results": results,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {output}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
