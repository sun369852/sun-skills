#!/usr/bin/env python3
"""Grade trigger eval results and write a Markdown report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Trigger eval JSON from run_trigger_eval_windows.py")
    parser.add_argument("--grading-output", required=True)
    parser.add_argument("--report-output", required=True)
    parser.add_argument("--description", default="", help="Optional description text or label")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    results = data.get("results", [])

    true_positive = sum(1 for item in results if item["should_trigger"] and item["triggered"])
    false_negative = sum(1 for item in results if item["should_trigger"] and not item["triggered"])
    true_negative = sum(1 for item in results if not item["should_trigger"] and not item["triggered"])
    false_positive = sum(1 for item in results if not item["should_trigger"] and item["triggered"])
    total = len(results)
    passed = true_positive + true_negative
    should_trigger_total = true_positive + false_negative
    should_not_total = true_negative + false_positive

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0
    recall = true_positive / should_trigger_total if should_trigger_total else 0
    specificity = true_negative / should_not_total if should_not_total else 0
    accuracy = passed / total if total else 0

    expectations = []
    for item in results:
        rate = item.get("trigger_rate")
        if rate is None:
            rate = 1.0 if item.get("triggered") else 0.0
        expected = "trigger" if item["should_trigger"] else "not trigger"
        actual = "triggered" if item["triggered"] else "did not trigger"
        expectations.append({
            "text": f"Eval {item.get('id')}: should {expected}",
            "passed": bool(item.get("passed")),
            "evidence": f"{actual}; trigger_rate={rate:.2f}; query={item['query']}",
        })

    grading = {
        "skill_name": data.get("skill_name"),
        "model": data.get("model"),
        "input": str(Path(args.input)),
        "graded_at": datetime.now().isoformat(timespec="seconds"),
        "summary": {
            "passed": passed,
            "total": total,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "specificity": specificity,
            "true_positive": true_positive,
            "false_negative": false_negative,
            "true_negative": true_negative,
            "false_positive": false_positive,
            "runs_per_query": data.get("runs_per_query", 1),
            "trigger_threshold": data.get("trigger_threshold", 0.5),
            "timeout_seconds": data.get("timeout_seconds"),
        },
        "expectations": expectations,
    }

    grading_output = Path(args.grading_output)
    grading_output.parent.mkdir(parents=True, exist_ok=True)
    grading_output.write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")

    failures = [item for item in results if not item.get("passed")]
    unstable = []
    for item in results:
        runs = item.get("runs", [])
        if runs:
            trigger_values = {run.get("triggered") for run in runs}
            if len(trigger_values) > 1:
                unstable.append(item)

    lines = [
        "# Description Trigger Evaluation Report",
        "",
        f"- Skill: `{data.get('skill_name')}`",
        f"- Model: `{data.get('model')}`",
        f"- Input: `{Path(args.input)}`",
        f"- Runs per query: `{data.get('runs_per_query', 1)}`",
        f"- Trigger threshold: `{data.get('trigger_threshold', 0.5)}`",
        f"- Timeout seconds: `{data.get('timeout_seconds')}`",
        f"- Generated: `{grading['graded_at']}`",
    ]
    if args.description:
        lines.append(f"- Description label: {args.description}")

    lines.extend([
        "",
        "## Summary",
        "",
        f"- Overall: `{passed}/{total}` ({pct(accuracy)})",
        f"- Precision: `{pct(precision)}`",
        f"- Recall: `{pct(recall)}`",
        f"- Specificity: `{pct(specificity)}`",
        f"- True positives: `{true_positive}`",
        f"- False negatives: `{false_negative}`",
        f"- True negatives: `{true_negative}`",
        f"- False positives: `{false_positive}`",
        "",
        "## Failures",
        "",
    ])

    if failures:
        for item in failures:
            lines.append(
                f"- Eval {item.get('id')}: expected `{item['should_trigger']}`, "
                f"actual `{item['triggered']}`, rate `{item.get('trigger_rate', 0):.2f}`"
            )
            lines.append(f"  Query: {item['query']}")
    else:
        lines.append("- None.")

    lines.extend(["", "## Unstable Items", ""])
    if unstable:
        for item in unstable:
            run_values = ", ".join(str(run.get("triggered")) for run in item.get("runs", []))
            lines.append(f"- Eval {item.get('id')}: trigger runs [{run_values}]")
            lines.append(f"  Query: {item['query']}")
    else:
        lines.append("- None detected across repeated runs.")

    lines.extend(["", "## Recommendation", ""])
    if false_positive:
        lines.append("- Tighten the description boundary because false positives are more harmful for this execution-only skill.")
    if false_negative and not false_positive:
        lines.append("- Consider adding narrow trigger phrases for missed positive cases, but avoid broad wording that pulls in PRD/design/task-generation requests.")
    if not failures:
        lines.append("- Keep the current description. No trigger changes are indicated by this eval set.")

    report_output = Path(args.report_output)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Grading: {grading_output}")
    print(f"Report: {report_output}")
    print(f"Overall: {passed}/{total} ({pct(accuracy)})")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
