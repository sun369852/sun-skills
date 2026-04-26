#!/usr/bin/env python3
"""Windows-compatible trigger evaluator for a skill description."""

import argparse
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple[str, str]:
    """读取 SKILL.md 中的名称和 description。"""
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("SKILL.md missing frontmatter")
    _, frontmatter, _ = text.split("---", 2)
    name = ""
    description = ""
    for line in frontmatter.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
    if not name or not description:
        raise ValueError("SKILL.md missing name or description")
    return name, description


def run_query(query: str, skill_name: str, description: str, project_root: Path, timeout: int, model: str | None) -> bool:
    """执行单条查询，并从 Claude stream-json 输出中判断是否触发临时 skill。"""
    clean_name = f"{skill_name}-skill-{uuid.uuid4().hex[:8]}"
    commands_dir = project_root / ".claude" / "commands"
    command_file = commands_dir / f"{clean_name}.md"
    commands_dir.mkdir(parents=True, exist_ok=True)

    indented_desc = "\n  ".join(description.splitlines())
    command_file.write_text(
        f"---\ndescription: |\n  {indented_desc}\n---\n\n# {skill_name}\n\nThis skill handles: {description}\n",
        encoding="utf-8",
    )

    cmd = [
        "claude",
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
    ]
    if model:
        cmd.extend(["--model", model])

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(project_root),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        stderr = exc.stderr or ""
    else:
        output = completed.stdout
        stderr = completed.stderr
    finally:
        command_file.unlink(missing_ok=True)

    if stderr and "error" in stderr.lower():
        print(stderr.strip()[:500], file=sys.stderr)

    return clean_name in output and ('"name":"Skill"' in output or '"name": "Skill"' in output or '"name":"Read"' in output or '"name": "Read"' in output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-set", required=True)
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    skill_name, description = parse_skill_md(Path(args.skill_path))
    project_root = Path(args.project_root).resolve()

    results = []
    for index, item in enumerate(eval_set, start=1):
        triggered = run_query(item["query"], skill_name, description, project_root, args.timeout, args.model)
        passed = triggered == item["should_trigger"]
        results.append({**item, "triggered": triggered, "pass": passed})
        status = "PASS" if passed else "FAIL"
        print(f"[{index:02d}] {status} triggered={triggered} expected={item['should_trigger']} {item['query'][:80]}")

    passed = sum(1 for result in results if result["pass"])
    summary = {"passed": passed, "total": len(results), "results": results}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
