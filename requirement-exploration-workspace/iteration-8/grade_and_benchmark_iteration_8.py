import json
import math
from datetime import datetime, UTC
from pathlib import Path

# 评测根目录：存放本轮 iteration-8 的所有 run、grading 与 benchmark 产物。
WORKSPACE = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-8")
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
                "evidence": "It stays focused on the highest-value missing product detail: what kind of site this is and what core rights paid members get.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": True,
                "evidence": "The response is short and centered on one clarification theme, without turning into a template or checklist.",
            },
        ],
        "without_skill": [
            {
                "text": "Does not immediately output a final downstream prompt in the first response",
                "passed": True,
                "evidence": "The baseline still asks for more information first and does not jump directly to final prompt generation.",
            },
            {
                "text": "Asks one focused clarification question about the highest-value missing product detail",
                "passed": True,
                "evidence": "It remains centered on the core gap of business type, target user, and member value.",
            },
            {
                "text": "Keeps the first response to one primary clarification theme rather than a multi-part intake form",
                "passed": False,
                "evidence": "It expands into a mini answer template with four bullet fields, so the first turn is no longer just one compact clarification prompt.",
            },
        ],
    },
    "approval-center-late-stage": {
        "with_skill": [
            {
                "text": "Uses the prior conversation as context instead of restarting requirement discovery from scratch",
                "passed": True,
                "evidence": "It continues from the existing approval-center discussion and performs a late-stage closeout review rather than restarting discovery.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "The reply separates confirmed rules, unresolved but non-blocking items, and possible rework risks before making a readiness judgment.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": True,
                "evidence": "It says the requirement is already complete enough to proceed and asks whether to generate now under an explicit assumption set.",
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
                "evidence": "It performs a concise closeout review and isolates one remaining potentially blocking issue instead of restarting requirement discovery from zero.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": False,
                "evidence": "It still asks one more clarification question about timeout handling instead of asking for permission to begin final generation now.",
            },
        ],
    },
    "incomplete-prd-late-stage": {
        "with_skill": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "The response continues from the existing subscription PRD draft context rather than restarting requirement discovery.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": False,
                "evidence": "It does not first review the confirmed rules versus remaining non-blocking gaps; instead it opens another bundled six-item clarification round.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": False,
                "evidence": "It requires the user to resolve six more rules before continuing, instead of offering generation now with pending assumptions.",
            },
        ],
        "without_skill": [
            {
                "text": "Treats the prior PRD draft discussion as authoritative input context rather than restarting from zero",
                "passed": True,
                "evidence": "The baseline continues directly from the existing PRD draft and references the already confirmed subscription rules.",
            },
            {
                "text": "Performs a gap review covering confirmed rules plus any remaining boundary, risk, or missing-decision items",
                "passed": True,
                "evidence": "It summarizes what is already confirmed and classifies the remaining timing and effective-date details as non-blocking pending items.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": True,
                "evidence": "It explicitly judges the requirement ready enough and asks whether to proceed with the more complete downstream prompt now.",
            },
        ],
    },
    "coupon-module-late-stage-defaults": {
        "with_skill": [
            {
                "text": "Continues from the late-stage coupon-module context instead of restarting requirement discovery",
                "passed": True,
                "evidence": "It continues from the near-complete coupon-module context and performs a late-stage review rather than restarting discovery.",
            },
            {
                "text": "Performs a review that separates confirmed coupon rules from unresolved but non-blocking boundary items",
                "passed": True,
                "evidence": "It summarizes the confirmed coupon rules first, then separates stacking, whitelist issuance, and redemption metrics as non-blocking pending boundaries.",
            },
            {
                "text": "Offers explicit generation authorization now instead of defaulting to another clarification round for remaining defaults",
                "passed": True,
                "evidence": "It states generation can begin now and asks whether to proceed as-is or first answer one preferred open point.",
            },
        ],
        "without_skill": [
            {
                "text": "Continues from the late-stage coupon-module context instead of restarting requirement discovery",
                "passed": True,
                "evidence": "The baseline also continues from the existing coupon-module context instead of resetting the discussion.",
            },
            {
                "text": "Performs a review that separates confirmed coupon rules from unresolved but non-blocking boundary items",
                "passed": False,
                "evidence": "It skips the confirmed-versus-unresolved review and jumps straight to proposing three default boundary decisions.",
            },
            {
                "text": "Offers explicit generation authorization now instead of defaulting to another clarification round for remaining defaults",
                "passed": False,
                "evidence": "It asks the user to approve its three default decisions before proceeding, so it still behaves like another clarification round.",
            },
        ],
    },
}

# 分析备注：总结本轮修补是否命中回归点，以及区分度如何变化。
ANALYST_NOTES = [
    "这次最小修补没有打中 incomplete-prd-late-stage：with_skill 仍然把 draft-based late-stage 场景重新拉回 bundled follow-up round。",
    "coupon-module-late-stage-defaults 仍然保持区分度：with_skill 是 review + readiness + authorization，baseline 还是先替用户拍默认口径。",
    "approval-center-late-stage 也依旧有效，但 baseline 已经会先做 closeout review，再追一个它认为更关键的剩余问题。",
    "short-membership-request 再次显示为回归保护样本：with_skill 保持短促，baseline 又轻微回到了模板化回答。",
    "当前主要瓶颈不是覆盖不到 late-stage，而是 draft-based late-stage 仍缺少更硬的反 bundled-round 约束。",
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
            "overall": "Manual grading for iteration-8 based on response.txt.",
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
            "# requirement-exploration iteration-8 benchmark",
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
