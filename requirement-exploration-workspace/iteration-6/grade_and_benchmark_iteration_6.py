import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev

# 固定本轮 workspace 路径，避免不同脚本间相对路径漂移。
ITERATION_DIR = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-6")
SKILL_PATH = "/c/Users/sun/.claude/skills/requirement-exploration"
SKILL_NAME = "requirement-exploration"

# 这里记录人工判分结论，用统一结构生成 grading 与 benchmark。
GRADES = {
    ("short-membership-request", "with_skill"): {
        "expectations": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The response asks for clarification first and does not generate the downstream prompt in the first turn.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It stays centered on the highest-value product framing gap: who the membership is for and what business goal it serves.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "The reply is shorter than iteration-5 and no longer expands into an example-filled intake template; it remains within one compact clarification theme.",
            },
        ],
        "overall": "The first-turn shape is back under control: still focused, but no longer reads like a small intake form.",
    },
    ("short-membership-request", "without_skill"): {
        "expectations": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The response asks for more information first and does not generate the downstream prompt.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It asks one compact question around what product this membership belongs to and what rights it grants.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "The reply remains concise and focused rather than turning into a checklist-style intake.",
            },
        ],
        "overall": "Baseline also stays compact and focused on one core clarification theme here.",
    },
    ("approval-center-late-stage", "with_skill"): {
        "expectations": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "It explicitly says it will not restart and continues from the existing approval-center context.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "It separates confirmed rules, unresolved points, and high-risk-but-non-blocking details in a structured review.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": True,
                "evidence": "It says the requirement is ready enough to proceed and asks whether to generate now or answer more open items first.",
            },
        ],
        "overall": "The late-stage review-first behavior remains stable in the approval-center scenario.",
    },
    ("approval-center-late-stage", "without_skill"): {
        "expectations": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "It continues from the current approval-center context instead of restarting from zero.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": False,
                "evidence": "It jumps straight to one more clarification question about single-level versus multi-level approval and does not first summarize confirmed information versus remaining gaps.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": False,
                "evidence": "It asks another follow-up question instead of requesting permission to begin final generation.",
            },
        ],
        "overall": "Baseline still falls back to one more blocker question instead of doing a proper late-stage review and authorization handoff.",
    },
    ("incomplete-prd-late-stage", "with_skill"): {
        "expectations": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "It continues directly from the existing PRD-draft context and references the rules that were already confirmed.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": True,
                "evidence": "It summarizes the confirmed subscription rules, separates non-blocking gaps, and labels them as details that can be carried as assumptions.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": True,
                "evidence": "It says there is no obvious blocking gap and asks directly whether it should begin the more complete PRD supplement now.",
            },
        ],
        "overall": "This fixes the draft-based late-stage failure: the remaining uncertainties are treated as non-blocking and the model asks for authorization now.",
    },
    ("incomplete-prd-late-stage", "without_skill"): {
        "expectations": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "It continues from the current PRD-draft context rather than restarting requirement discovery from zero.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": True,
                "evidence": "It summarizes the confirmed rules and then lists a set of remaining non-blocking details that can be supplemented later.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": True,
                "evidence": "It says there is no obvious blocking gap and explicitly asks whether to continue based on the current information.",
            },
        ],
        "overall": "Baseline also improved substantially in this draft-based late-stage scenario and now reaches an authorization handoff without the skill.",
    },
}


def read_json(path: Path) -> dict:
    # 统一读取 UTF-8 JSON，减少每处重复样板。
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    # 所有输出都保留中文与缩进，便于后续人工检查。
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def summarize_expectations(expectations: list[dict]) -> dict:
    # 根据断言通过情况生成 pass/fail 汇总。
    passed = sum(1 for item in expectations if item["passed"])
    total = len(expectations)
    failed = total - passed
    return {
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": round(passed / total, 2),
    }


def build_grading(eval_name: str, config: str) -> dict:
    # 生成与 viewer 兼容的 grading.json 结构。
    grade = GRADES[(eval_name, config)]
    run_dir = ITERATION_DIR / eval_name / config
    timing = read_json(run_dir / "timing.json")
    response = (run_dir / "outputs" / "response.txt").read_text(encoding="utf-8")
    summary = summarize_expectations(grade["expectations"])
    return {
        "expectations": grade["expectations"],
        "summary": summary,
        "execution_metrics": {
            "tool_calls": {},
            "total_tool_calls": 0,
            "total_steps": 1,
            "errors_encountered": 0,
            "output_chars": len(response),
            "transcript_chars": 0,
        },
        "timing": {
            "executor_duration_seconds": timing["total_duration_seconds"],
            "grader_duration_seconds": 0.0,
            "total_duration_seconds": timing["total_duration_seconds"],
        },
        "claims": [],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": [],
            "workarounds": [],
        },
        "eval_feedback": {
            "suggestions": [],
            "overall": grade["overall"],
        },
    }


def stats(values: list[float]) -> dict:
    # 用总体标准差与历史 benchmark 保持一致。
    return {
        "mean": round(mean(values), 2),
        "stddev": round(pstdev(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
    }


def signed_delta(current: float, baseline: float, digits: int = 2) -> str:
    # benchmark 里 delta 保持显式正负号，便于快速比较。
    diff = round(current - baseline, digits)
    return f"{diff:+.{digits}f}"


def main() -> None:
    # 先写每个 run 的 grading，再聚合整个 iteration 的 benchmark。
    eval_names = [
        "short-membership-request",
        "approval-center-late-stage",
        "incomplete-prd-late-stage",
    ]
    configs = ["with_skill", "without_skill"]

    runs = []
    summary_values = {config: {"pass_rate": [], "time_seconds": [], "tokens": []} for config in configs}

    for eval_id, eval_name in enumerate(eval_names):
        for config in configs:
            grading = build_grading(eval_name, config)
            write_json(ITERATION_DIR / eval_name / config / "grading.json", grading)

            timing = read_json(ITERATION_DIR / eval_name / config / "timing.json")
            run_entry = {
                "eval_id": eval_id,
                "eval_name": eval_name,
                "configuration": config,
                "run_number": 1,
                "result": {
                    "pass_rate": grading["summary"]["pass_rate"],
                    "passed": grading["summary"]["passed"],
                    "failed": grading["summary"]["failed"],
                    "total": grading["summary"]["total"],
                    "time_seconds": timing["total_duration_seconds"],
                    "tokens": 0,
                    "tool_calls": 0,
                    "errors": 0,
                },
                "expectations": grading["expectations"],
                "notes": [],
            }
            runs.append(run_entry)
            summary_values[config]["pass_rate"].append(run_entry["result"]["pass_rate"])
            summary_values[config]["time_seconds"].append(run_entry["result"]["time_seconds"])
            summary_values[config]["tokens"].append(0.0)

    with_skill_pass = mean(summary_values["with_skill"]["pass_rate"])
    baseline_pass = mean(summary_values["without_skill"]["pass_rate"])
    with_skill_time = mean(summary_values["with_skill"]["time_seconds"])
    baseline_time = mean(summary_values["without_skill"]["time_seconds"])

    benchmark = {
        "metadata": {
            "skill_name": SKILL_NAME,
            "skill_path": SKILL_PATH,
            "executor_model": "claude-opus-4-6",
            "analyzer_model": "gpt-5.4",
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "evals_run": [0, 1, 2],
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": {
            "with_skill": {
                "pass_rate": stats(summary_values["with_skill"]["pass_rate"]),
                "time_seconds": stats(summary_values["with_skill"]["time_seconds"]),
                "tokens": stats(summary_values["with_skill"]["tokens"]),
            },
            "without_skill": {
                "pass_rate": stats(summary_values["without_skill"]["pass_rate"]),
                "time_seconds": stats(summary_values["without_skill"]["time_seconds"]),
                "tokens": stats(summary_values["without_skill"]["tokens"]),
            },
            "delta": {
                "pass_rate": signed_delta(with_skill_pass, baseline_pass),
                "time_seconds": signed_delta(with_skill_time, baseline_time),
                "tokens": "+0",
            },
        },
        "notes": [
            "short-membership-request 修回来了：with_skill 首轮回复不再展开成小型答题模板，而是保持短促单主题提问。",
            "incomplete-prd-late-stage 也修回来了：with_skill 终于把剩余边界当作非阻塞项处理，并明确征求是否现在开始生成。",
            "但 baseline 在 incomplete-prd-late-stage 也同步变强，说明这个用例对当前 skill 的区分度正在下降。",
            "approval-center-late-stage 仍然是当前最稳定的区分项：with_skill 能 review + readiness + authorization，而 baseline 仍倾向继续追一个问题。",
        ],
    }
    write_json(ITERATION_DIR / "benchmark.json", benchmark)

    benchmark_md = "\n".join([
        "# requirement-exploration iteration-6 benchmark",
        "",
        f"- with_skill mean pass_rate: {benchmark['run_summary']['with_skill']['pass_rate']['mean']}",
        f"- without_skill mean pass_rate: {benchmark['run_summary']['without_skill']['pass_rate']['mean']}",
        f"- delta pass_rate: {benchmark['run_summary']['delta']['pass_rate']}",
        f"- with_skill mean time_seconds: {benchmark['run_summary']['with_skill']['time_seconds']['mean']}",
        f"- without_skill mean time_seconds: {benchmark['run_summary']['without_skill']['time_seconds']['mean']}",
        f"- delta time_seconds: {benchmark['run_summary']['delta']['time_seconds']}",
        "",
        "## Notes",
        "- short-membership-request 修回来了：with_skill 首轮回复不再展开成小型答题模板，而是保持短促单主题提问。",
        "- incomplete-prd-late-stage 也修回来了：with_skill 终于把剩余边界当作非阻塞项处理，并明确征求是否现在开始生成。",
        "- 但 baseline 在 incomplete-prd-late-stage 也同步变强，说明这个用例对当前 skill 的区分度正在下降。",
        "- approval-center-late-stage 仍然是当前最稳定的区分项：with_skill 能 review + readiness + authorization，而 baseline 仍倾向继续追一个问题。",
        "",
    ])
    (ITERATION_DIR / "benchmark.md").write_text(benchmark_md, encoding="utf-8")


if __name__ == "__main__":
    main()
