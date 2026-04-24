import json
import math
from datetime import datetime, UTC
from pathlib import Path

# 评测根目录：存放本轮 iteration-7 的所有 run、grading 与 benchmark 产物。
WORKSPACE = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-7")
SKILL_NAME = "requirement-exploration"
SKILL_PATH = "/c/Users/sun/.claude/skills/requirement-exploration"

# 人工判分结果：基于本轮 response.txt 对每个断言逐项判断。
GRADING_SPECS = {
    "short-membership-request": {
        "with_skill": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The reply asks one clarification question first and does not generate any downstream prompt in the opening turn.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It focuses on the highest-value missing detail: who the membership is for and what core value the paid plan grants.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "The response stays compact and centered on a single clarification theme instead of expanding into a mini intake template.",
            },
        ],
        "without_skill": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The baseline also asks for more product detail first and does not jump straight to final prompt generation.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It still centers on one core gap: target user and member rights, which are the highest-value missing inputs.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "Although it includes examples in parentheses, it remains one compact question rather than a checklist-style intake round.",
            },
        ],
    },
    "approval-center-late-stage": {
        "with_skill": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "It explicitly performs a late-stage review based on the already confirmed approval-center discussion and does not restart discovery.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "The response lists confirmed scope and rules first, then separates unresolved items as non-blocking and calls out the possible rework risk if they stay undecided.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": True,
                "evidence": "It judges the requirement ready enough to proceed and directly asks whether to continue generation now with the open items marked as pending.",
            },
        ],
        "without_skill": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "The baseline continues from the current approval-center context rather than reopening the whole discovery flow.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "It summarizes the confirmed V1 scope and explicitly treats transfer, countersign, and withdraw as non-blocking pending items before raising one more question.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": False,
                "evidence": "It still asks one more scope question about whether downstream execution stays inside the same system, rather than asking for permission to start final generation now.",
            },
        ],
    },
    "incomplete-prd-late-stage": {
        "with_skill": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "The response continues from the existing subscription PRD draft instead of restarting requirement discovery from scratch.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": False,
                "evidence": "It says the draft is almost enough, but then jumps into a new five-item clarification round without first reviewing the confirmed rules versus the remaining non-blocking edges.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": False,
                "evidence": "Instead of offering generation authorization, it tells the user to resolve five more points before it will continue.",
            },
        ],
        "without_skill": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "The baseline continues directly from the current PRD draft context and references the confirmed subscription rules already established in the dialogue.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": True,
                "evidence": "It summarizes the confirmed rules, separates the remaining details as non-blocking assumptions or pending items, and avoids reopening broad discovery.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": True,
                "evidence": "It states there is no obvious blocking gap and explicitly asks whether to continue generating the more complete next version based on the current information.",
            },
        ],
    },
    "coupon-module-late-stage-defaults": {
        "with_skill": [
            {
                "text": "Continues from the late-stage coupon-module context instead of restarting requirement discovery",
                "passed": True,
                "evidence": "The response picks up from the near-complete coupon-module conversation and continues with a late-stage review rather than restarting discovery.",
            },
            {
                "text": "Performs a review that separates confirmed coupon rules from unresolved but non-blocking boundary items",
                "passed": True,
                "evidence": "It summarizes the confirmed coupon scope and rules first, then identifies stacking, whitelist issuance, and write-off metrics as unresolved but still non-blocking boundary items.",
            },
            {
                "text": "Offers explicit generation authorization now instead of defaulting to another clarification round for remaining defaults",
                "passed": True,
                "evidence": "It judges the requirement ready enough and asks whether to proceed now while marking the three open points as pending boundaries.",
            },
        ],
        "without_skill": [
            {
                "text": "Continues from the late-stage coupon-module context instead of restarting requirement discovery",
                "passed": True,
                "evidence": "The baseline also continues from the existing coupon-module context rather than resetting the conversation.",
            },
            {
                "text": "Performs a review that separates confirmed coupon rules from unresolved but non-blocking boundary items",
                "passed": False,
                "evidence": "It moves straight into proposing three default decisions and does not first provide a clear confirmed-versus-unresolved review of the current coupon rules.",
            },
            {
                "text": "Offers explicit generation authorization now instead of defaulting to another clarification round for remaining defaults",
                "passed": False,
                "evidence": "It asks the user to approve the three default boundaries before proceeding, so it still behaves like another clarification round instead of offering generation now with assumptions.",
            },
        ],
    },
}

# 分析备注：总结本轮区分度、回归点与时间代价。
ANALYST_NOTES = [
    "coupon-module-late-stage-defaults 成功补到了新的区分盲点：with_skill 能 review + readiness + authorization，baseline 仍倾向先替用户拍默认口径再继续。",
    "incomplete-prd-late-stage 出现反向结果：with_skill 重新滑回多点补问，baseline 反而完成了 review + non-blocking + authorization，说明 draft-based late-stage 行为仍不稳定。",
    "approval-center-late-stage 仍有区分度，但 baseline 比上一轮更强，已经会先做简版 review，再追一个它认为阻塞的问题。",
    "short-membership-request 继续不具备区分度：两边首轮都足够克制，说明这个样本现在更像回归保护而不是拉开差距的主力样本。",
    "本轮 with_skill 平均耗时高于 baseline，说明当前收益问题既有 late-stage 规则稳定性，也有一定的额外交互成本。",
]


def round2(value: float) -> float:
    return round(value + 1e-12, 2)


def make_grading(expectations: list[dict], timing: dict) -> dict:
    passed = sum(1 for item in expectations if item["passed"])
    total = len(expectations)
    failed = total - passed
    pass_rate = passed / total if total else 0.0
    duration = timing.get("executor_duration_seconds", timing.get("total_duration_seconds", 0.0))
    return {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": round2(pass_rate),
        },
        "execution_metrics": {
            "tool_calls": {},
            "total_tool_calls": 0,
            "total_steps": 1,
            "errors_encountered": 0,
            "output_chars": 0,
            "transcript_chars": 0,
        },
        "timing": {
            "executor_duration_seconds": duration,
            "grader_duration_seconds": 0.0,
            "total_duration_seconds": duration,
        },
        "claims": [],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": [],
            "workarounds": [],
        },
        "eval_feedback": {
            "suggestions": [],
            "overall": "Manual grading for iteration-7 based on response.txt.",
        },
    }


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def stat_block(values: list[float]) -> dict:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return {
        "mean": round2(mean),
        "stddev": round2(math.sqrt(variance)),
        "min": round2(min(values)),
        "max": round2(max(values)),
    }


def build_run_entry(eval_id: int, eval_name: str, configuration: str, grading: dict, timing: dict) -> dict:
    duration = timing.get("executor_duration_seconds", timing.get("total_duration_seconds", 0.0))
    return {
        "eval_id": eval_id,
        "eval_name": eval_name,
        "configuration": configuration,
        "run_number": 1,
        "result": {
            "pass_rate": grading["summary"]["pass_rate"],
            "passed": grading["summary"]["passed"],
            "failed": grading["summary"]["failed"],
            "total": grading["summary"]["total"],
            "time_seconds": round2(duration),
            "tokens": timing.get("total_tokens", 0),
            "tool_calls": grading["execution_metrics"]["total_tool_calls"],
            "errors": grading["execution_metrics"]["errors_encountered"],
        },
        "expectations": grading["expectations"],
        "notes": [],
    }


def main() -> None:
    runs = []
    with_skill_pass_rates = []
    without_skill_pass_rates = []
    with_skill_times = []
    without_skill_times = []
    with_skill_tokens = []
    without_skill_tokens = []
    eval_ids = []

    for eval_name, config_specs in GRADING_SPECS.items():
        metadata = read_json(WORKSPACE / eval_name / "eval_metadata.json")
        eval_id = metadata["eval_id"]
        eval_ids.append(eval_id)

        for configuration in ["with_skill", "without_skill"]:
            run_dir = WORKSPACE / eval_name / configuration
            timing = read_json(run_dir / "timing.json")
            grading = make_grading(config_specs[configuration], timing)
            (run_dir / "grading.json").write_text(
                json.dumps(grading, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            run_entry = build_run_entry(eval_id, eval_name, configuration, grading, timing)
            runs.append(run_entry)

            if configuration == "with_skill":
                with_skill_pass_rates.append(run_entry["result"]["pass_rate"])
                with_skill_times.append(run_entry["result"]["time_seconds"])
                with_skill_tokens.append(run_entry["result"]["tokens"])
            else:
                without_skill_pass_rates.append(run_entry["result"]["pass_rate"])
                without_skill_times.append(run_entry["result"]["time_seconds"])
                without_skill_tokens.append(run_entry["result"]["tokens"])

    benchmark = {
        "metadata": {
            "skill_name": SKILL_NAME,
            "skill_path": SKILL_PATH,
            "executor_model": "claude-opus-4-6",
            "analyzer_model": "gpt-5.4",
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "evals_run": sorted(eval_ids),
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": {
            "with_skill": {
                "pass_rate": stat_block(with_skill_pass_rates),
                "time_seconds": stat_block(with_skill_times),
                "tokens": stat_block(with_skill_tokens),
            },
            "without_skill": {
                "pass_rate": stat_block(without_skill_pass_rates),
                "time_seconds": stat_block(without_skill_times),
                "tokens": stat_block(without_skill_tokens),
            },
            "delta": {
                "pass_rate": f"{sum(with_skill_pass_rates) / len(with_skill_pass_rates) - sum(without_skill_pass_rates) / len(without_skill_pass_rates):+0.2f}",
                "time_seconds": f"{sum(with_skill_times) / len(with_skill_times) - sum(without_skill_times) / len(without_skill_times):+0.2f}",
                "tokens": f"{sum(with_skill_tokens) / len(with_skill_tokens) - sum(without_skill_tokens) / len(without_skill_tokens):+0.0f}",
            },
        },
        "notes": ANALYST_NOTES,
    }

    (WORKSPACE / "benchmark.json").write_text(
        json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    benchmark_md = "\n".join(
        [
            "# requirement-exploration iteration-7 benchmark",
            "",
            f"- with_skill mean pass_rate: {benchmark['run_summary']['with_skill']['pass_rate']['mean']}",
            f"- without_skill mean pass_rate: {benchmark['run_summary']['without_skill']['pass_rate']['mean']}",
            f"- delta pass_rate: {benchmark['run_summary']['delta']['pass_rate']}",
            f"- with_skill mean time_seconds: {benchmark['run_summary']['with_skill']['time_seconds']['mean']}",
            f"- without_skill mean time_seconds: {benchmark['run_summary']['without_skill']['time_seconds']['mean']}",
            f"- delta time_seconds: {benchmark['run_summary']['delta']['time_seconds']}",
            "",
            "## Notes",
            *[f"- {note}" for note in ANALYST_NOTES],
            "",
        ]
    )
    (WORKSPACE / "benchmark.md").write_text(benchmark_md, encoding="utf-8")


if __name__ == "__main__":
    main()
