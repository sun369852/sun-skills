import json
import subprocess
import time
from pathlib import Path

# 评测根目录：存放本轮 iteration-13 的所有 eval run 输出。
WORKSPACE = Path(r"C:\Users\sun\.claude\skills\requirement-exploration-workspace\iteration-13")
SKILL_NAME = "requirement-exploration"
COMMAND = [
    "claude",
    "-p",
    "--output-format",
    "text",
    "--permission-mode",
    "bypassPermissions",
]


def load_eval_metadata(eval_dir: Path) -> dict:
    return json.loads((eval_dir / "eval_metadata.json").read_text(encoding="utf-8"))


def build_input(prompt: str, config: str) -> str:
    if config == "with_skill":
        return f"/{SKILL_NAME}\n\n{prompt}"
    return prompt


def run_case(eval_dir: Path, config: str) -> None:
    metadata = load_eval_metadata(eval_dir)
    run_dir = eval_dir / config
    outputs_dir = run_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    task_input = build_input(metadata["prompt"], config)
    start = time.time()
    result = subprocess.run(
        COMMAND,
        input=task_input,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    end = time.time()

    response_text = result.stdout if result.stdout else result.stderr
    (outputs_dir / "response.txt").write_text(response_text, encoding="utf-8")

    run_json = {
        "returncode": result.returncode,
        "stdout_chars": len(result.stdout),
        "stderr_chars": len(result.stderr),
        "command": COMMAND,
        "config": config,
        "eval_id": metadata["eval_id"],
        "eval_dir": str(eval_dir),
    }
    (run_dir / "run.json").write_text(json.dumps(run_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    duration = round(end - start, 3)
    timing_json = {
        "total_tokens": 0,
        "duration_ms": round((end - start) * 1000),
        "total_duration_seconds": duration,
        "executor_start": start,
        "executor_end": end,
        "executor_duration_seconds": duration,
    }
    (run_dir / "timing.json").write_text(json.dumps(timing_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    eval_names = [
        "short-membership-request",
        "approval-center-late-stage",
        "incomplete-prd-late-stage",
        "coupon-module-late-stage-defaults",
        "pricing-plan-late-stage-authorization",
        "content-permission-late-stage-boundaries",
        "certificate-module-single-blocking-gap",
        "event-registration-vague-authorization",
    ]
    for eval_name in eval_names:
        eval_dir = WORKSPACE / eval_name
        for config in ["with_skill", "without_skill"]:
            run_case(eval_dir, config)
