import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev

# 固定本轮 workspace 路径，避免不同脚本间相对路径漂移。
ITERATION_DIR = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-5")
SKILL_PATH = "/c/Users/sun/.claude/skills/requirement-exploration"
SKILL_NAME = "requirement-exploration"

# 这里记录人工判分结论，用统一结构生成 grading 与 benchmark。
GRADES = {
    ("short-membership-request", "with_skill"): {
        "expectations": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The response asks for clarification and does not generate the downstream prompt in the first turn.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It stays on the highest-value theme: what product the membership belongs to and what benefits it provides.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": False,
                "evidence": "It stays on one theme, but the reply expands into a mini answer template with multiple fields and an example, making it more form-like than the desired first-turn restraint.",
            },
        ],
        "overall": "Still restrained enough to avoid premature generation, but the first-turn shape drifted toward a mini intake form.",
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
                "evidence": "It stays centered on what product the membership serves and what the user gets after paying.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "Although it suggests a compact answer format, the response remains short and within one clarification theme rather than becoming a broad questionnaire.",
            },
        ],
        "overall": "Baseline remains compact and focused on one primary product-rights clarification theme.",
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
                "evidence": "It separates confirmed information from non-blocking gaps, proposed defaults, and unresolved details.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": True,
                "evidence": "It offers a direct handoff: either generate now with stated defaults or answer one last point first.",
            },
        ],
        "overall": "The new late-stage branch works here: review first, defaults explicit, and authorization is requested before generation.",
    },
    ("approval-center-late-stage", "without_skill"): {
        "expectations": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "It continues from the prior conversation and references the already-confirmed workflow rules.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "It briefly identifies non-blocking items, then isolates one remaining blocker instead of restarting discovery.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": False,
                "evidence": "It still asks one more blocking clarification question rather than requesting permission to begin generation now.",
            },
        ],
        "overall": "Baseline still shows the natural summarize-then-ask-one-blocker pattern, without explicit generation authorization.",
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
                "evidence": "It summarizes the confirmed subscription rules first, then isolates one remaining boundary around coexistence with single-course purchases.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": False,
                "evidence": "It still reclassifies the remaining boundary as a blocking question and asks the user to decide it first, instead of offering permission to generate now with explicit assumptions.",
            },
        ],
        "overall": "Structure remains better than baseline, but the new non-blocking branch still does not reliably fire in this draft-based late-stage scenario.",
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
                "passed": False,
                "evidence": "It jumps into another list of follow-up items instead of first summarizing confirmed rules and then reviewing the remaining gaps.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": False,
                "evidence": "It proposes five more questions and says it can continue after defaults are given, but it does not ask for permission to generate now.",
            },
        ],
        "overall": "Baseline remains in late-stage gap-filling mode rather than shifting to readiness judgment and authorization.",
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
        metadata = read_json(ITERATION_DIR / eval_name / "eval_metadata.json")
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
            "approval-center-late-stage 保住了 iteration-4 的修复：with_skill 仍然先 review，再给默认边界并征求是否直接生成。",
            "但 incomplete-prd-late-stage 依然没有恢复到 iteration-3 的双路径收口：with_skill 还是把剩余边界重新判成阻塞问题，未触发'现在也可生成'的授权。",
            "short-membership-request 这一轮 with_skill 略有回退，首轮回复仍克制，但更像小型答题模板；baseline 反而更紧凑。",
            "下一步更适合继续收紧 blocking gap 的判定口径：如果剩余问题可以显式写成默认假设或待确认项，就不要再把它升级成阻塞问题。",
        ],
    }
    write_json(ITERATION_DIR / "benchmark.json", benchmark)

    benchmark_md = "\n".join([
        "# requirement-exploration iteration-5 benchmark",
        "",
        f"- with_skill mean pass_rate: {benchmark['run_summary']['with_skill']['pass_rate']['mean']}",
        f"- without_skill mean pass_rate: {benchmark['run_summary']['without_skill']['pass_rate']['mean']}",
        f"- delta pass_rate: {benchmark['run_summary']['delta']['pass_rate']}",
        f"- with_skill mean time_seconds: {benchmark['run_summary']['with_skill']['time_seconds']['mean']}",
        f"- without_skill mean time_seconds: {benchmark['run_summary']['without_skill']['time_seconds']['mean']}",
        f"- delta time_seconds: {benchmark['run_summary']['delta']['time_seconds']}",
        "",
        "## Notes",
        "- approval-center-late-stage 保住了 iteration-4 的修复：with_skill 仍然先 review，再给默认边界并征求是否直接生成。",
        "- 但 incomplete-prd-late-stage 依然没有恢复到 iteration-3 的双路径收口：with_skill 还是把剩余边界重新判成阻塞问题，未触发‘现在也可生成’的授权。",
        "- short-membership-request 这一轮 with_skill 略有回退，首轮回复仍克制，但更像小型答题模板；baseline 反而更紧凑。",
        "- 当前最值得改的不是继续加新规则，而是把 blocking gap 的判定再收紧：只有不回答就会让最终 prompt 明显失真时，才允许 late-stage 继续追问。",
        "",
    ])
    (ITERATION_DIR / "benchmark.md").write_text(benchmark_md, encoding="utf-8")


if __name__ == "__main__":
    main()
