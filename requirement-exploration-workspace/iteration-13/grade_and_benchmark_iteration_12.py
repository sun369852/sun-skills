import json
import math
from datetime import datetime, UTC
from pathlib import Path

# 评测根目录：存放本轮 iteration-13 的所有 run、grading 与 benchmark 产物。
WORKSPACE = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-13")
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
                "passed": True,
                "evidence": "It asks a single focused question about target users and core member value, without expanding into a template or checklist.",
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
                "evidence": "It gives a closeout recap of the confirmed approval flow, surfaces one remaining boundary as the main possible rework risk, and frames the rest as non-blocking items that can be carried into the next draft.",
            },
            {
                "text": "Provides a pre-generation review that separates confirmed points from unresolved or risky items",
                "passed": True,
                "evidence": "It performs a concise closeout review and isolates one remaining potentially blocking issue instead of restarting requirement discovery from zero.",
            },
            {
                "text": "Asks explicitly whether to begin final downstream-prompt generation instead of generating immediately after '差不多了'",
                "passed": False,
                "evidence": "After the recap it asks the user to answer one more boundary question about whether V1 should enforce single-level approval, instead of asking whether to begin the final downstream generation now.",
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
                "passed": True,
                "evidence": "It reviews what is already confirmed about the subscription offering, classifies the remaining reminder, refund, timing, and coexistence edges as non-blocking assumptions, and says the current information is enough to continue.",
            },
            {
                "text": "Makes a readiness judgment and explicitly asks for permission before generating the final downstream prompt",
                "passed": True,
                "evidence": "It explicitly judges the requirement ready enough to continue and asks whether to proceed with the next version based on the confirmed information plus stated assumptions.",
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
                "passed": True,
                "evidence": "It summarizes the remaining coupon boundary items, explains which one is most likely to cause rework, and still treats the set as non-blocking for moving forward.",
            },
            {
                "text": "Offers explicit generation authorization now instead of defaulting to another clarification round for remaining defaults",
                "passed": True,
                "evidence": "It says the requirement is already complete enough and offers to continue drafting now under default assumptions if the remaining four boundary items are still undecided.",
            },
        ],
    },
    "pricing-plan-late-stage-authorization": {
        "with_skill": [
            {
                "text": "Continues from the late-stage pricing-plan context instead of reopening discovery from scratch",
                "passed": True,
                "evidence": "It stays inside the existing pricing-plan conversation and treats the remaining work as late-stage cleanup rather than restarting discovery.",
            },
            {
                "text": "Performs a review that separates confirmed pricing rules from unresolved but non-blocking commercial boundaries",
                "passed": True,
                "evidence": "It identifies the four remaining undecided commercial items as non-blocking pending rules and says the rest of the pricing scope is already sufficient to continue.",
            },
            {
                "text": "Asks for explicit generation authorization now instead of requiring approval of several default pricing decisions first",
                "passed": True,
                "evidence": "After the late-stage review it says generation can start now and explicitly conditions the next step on user agreement: '如果你同意，我就按当前已确认内容生成下一版，并把上述未定项单列为待确认清单。'",
            },
        ],
        "without_skill": [
            {
                "text": "Continues from the late-stage pricing-plan context instead of reopening discovery from scratch",
                "passed": True,
                "evidence": "The baseline continues directly from the existing pricing-plan conversation and performs a late-stage closeout review instead of restarting intake.",
            },
            {
                "text": "Performs a review that separates confirmed pricing rules from unresolved but non-blocking commercial boundaries",
                "passed": True,
                "evidence": "It lists the confirmed pricing scope and rules first, then isolates the unresolved commercial items as non-blocking pending decisions or default assumptions.",
            },
            {
                "text": "Asks for explicit generation authorization now instead of requiring approval of several default pricing decisions first",
                "passed": True,
                "evidence": "It explicitly asks whether to generate the next version now after surfacing the unresolved items, instead of making the user settle them all first.",
            },
        ],
    },
    "content-permission-late-stage-boundaries": {
        "with_skill": [
            {
                "text": "Treats the prior content-permission PRD draft as authoritative late-stage context rather than restarting discovery",
                "passed": True,
                "evidence": "It continues from the existing PRD-draft context and performs a closeout check on top of the confirmed permission rules rather than restarting the exploration flow.",
            },
            {
                "text": "Performs a closeout review that separates confirmed permission rules from remaining boundary or assumption items",
                "passed": True,
                "evidence": "It lists the already confirmed permission rules, then separates one potentially blocking item from several explicitly non-blocking boundary questions.",
            },
            {
                "text": "Makes a readiness judgment and asks whether to generate now instead of reopening a bundled follow-up round",
                "passed": True,
                "evidence": "It says the current information is close to ready, proposes one default assumption, and asks whether to proceed with the next draft now.",
            },
        ],
        "without_skill": [
            {
                "text": "Treats the prior content-permission PRD draft as authoritative late-stage context rather than restarting discovery",
                "passed": True,
                "evidence": "The baseline also continues directly from the content-permission PRD draft and does not reset the conversation from scratch.",
            },
            {
                "text": "Performs a closeout review that separates confirmed permission rules from remaining boundary or assumption items",
                "passed": False,
                "evidence": "Instead of doing a closeout review first, it jumps straight into drafting a detailed PRD-style rule set and only appends a few suggested follow-up points at the end.",
            },
            {
                "text": "Makes a readiness judgment and asks whether to generate now instead of reopening a bundled follow-up round",
                "passed": False,
                "evidence": "It does not ask whether to proceed; it directly generates the next-stage structured draft on its own.",
            },
        ],
    },
    "certificate-module-single-blocking-gap": {
        "with_skill": [
            {
                "text": "Treats the conversation as late-stage and continues from the existing certificate-module context",
                "passed": True,
                "evidence": "It continues from the near-complete certificate-module context and performs a late-stage closeout review instead of restarting discovery.",
            },
            {
                "text": "Identifies the unresolved rename-and-regeneration rule as one clearly blocking gap and explains why it blocks reliable generation",
                "passed": True,
                "evidence": "It explicitly identifies the rename-and-regeneration rule as the one real blocking gap and explains that it changes whether certificates are treated as historical snapshots, how reissue works, and how the audit trail should be interpreted.",
            },
            {
                "text": "Asks exactly one blocking clarification question instead of bundling more follow-up questions or moving straight into generation",
                "passed": True,
                "evidence": "It asks exactly one follow-up question focused on the blocking rename-and-regeneration rule, presents bounded options, and stops there instead of asking for generation authorization or bundling more cleanup questions.",
            },
        ],
        "without_skill": [
            {
                "text": "Treats the conversation as late-stage and continues from the existing certificate-module context",
                "passed": True,
                "evidence": "The baseline also continues from the existing certificate-module discussion rather than restarting discovery from scratch.",
            },
            {
                "text": "Identifies the unresolved rename-and-regeneration rule as one clearly blocking gap and explains why it blocks reliable generation",
                "passed": False,
                "evidence": "It surfaces the rename-and-regeneration rule as a remaining decision, but treats it as something that can be deferred into a pending decision list rather than a blocking prerequisite for reliable output.",
            },
            {
                "text": "Asks exactly one blocking clarification question instead of bundling more follow-up questions or moving straight into generation",
                "passed": False,
                "evidence": "It does not ask any blocking clarification question; it directly says it will mark the unresolved rule as pending and continue the next-stage write-up.",
            },
        ],
    },
    "event-registration-vague-authorization": {
        "with_skill": [
            {
                "text": "Continues from the late-stage event-registration context instead of restarting discovery",
                "passed": True,
                "evidence": "It continues from the existing late-stage event-registration review instead of reopening requirement discovery.",
            },
            {
                "text": "Recognizes that 你觉得行就行 is vague approval rather than explicit generation authorization",
                "passed": True,
                "evidence": "It does not treat '你觉得行就行' as sufficient authorization and instead asks for a clearer explicit go-ahead.",
            },
            {
                "text": "Asks again for explicit permission before generating instead of starting the final downstream prompt",
                "passed": True,
                "evidence": "It stops and asks the user to reply with an explicit authorization phrase such as '开始生成' before it will continue.",
            },
        ],
        "without_skill": [
            {
                "text": "Continues from the late-stage event-registration context instead of restarting discovery",
                "passed": True,
                "evidence": "The baseline also continues from the existing late-stage event-registration context rather than restarting discovery.",
            },
            {
                "text": "Recognizes that 你觉得行就行 is vague approval rather than explicit generation authorization",
                "passed": False,
                "evidence": "It treats the user's vague response as enough consent and immediately continues into a generated downstream prompt.",
            },
            {
                "text": "Asks again for explicit permission before generating instead of starting the final downstream prompt",
                "passed": False,
                "evidence": "It does not ask again for explicit permission; it starts producing the final downstream prompt immediately.",
            },
        ],
    }
}

# 分析备注：总结本轮修补是否命中回归点，以及区分度如何变化。
ANALYST_NOTES = [
    "最小补丁命中了新增的 certificate-module-single-blocking-gap：with_skill 不再把会改变证书历史含义的改名重发规则降级成 non-blocking，而是停在单个阻塞问题上。",
    "event-registration-vague-authorization 仍然通过，说明这次修补没有破坏明确授权边界。",
    "content-permission-late-stage-boundaries 继续保持 late-stage closeout + 单阻塞问题模式，没有被误放大成重新开一轮 discovery。",
    "coupon-module-late-stage-defaults 仍按非阻塞待确认项处理，说明本轮补丁没有把一般默认项误升级为 blocking。",
    "下一步若继续迭代，重点应从‘blocking gap 定义是否过宽’转向‘这条新规则在更多身份/历史语义样本上是否稳定’。",
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
            "overall": "Manual grading for iteration-13 based on response.txt.",
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
            "# requirement-exploration iteration-13 benchmark",
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
