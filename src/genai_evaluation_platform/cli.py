from __future__ import annotations

import argparse
import secrets
from pathlib import Path

import uvicorn

from .config import settings
from .runner import evaluate_suite, weak_baseline, write_report


def init_env() -> None:
    target = Path(".env")
    if target.exists():
        raise SystemExit("Error: .env already exists; existing files are never overwritten.")
    target.write_text(
        "GENAI_EVAL_API_KEY="
        + secrets.token_urlsafe(24)
        + "\nGENAI_EVAL_REQUESTS_PER_MINUTE=30\nGENAI_EVAL_PASS_THRESHOLD=0.80\n"
    )
    print("Created .env with a private random API key. Existing files are never overwritten.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="genai-eval")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("evaluate", "compare"):
        command = commands.add_parser(name)
        command.add_argument("--suite", default="eval/sample_suite.jsonl")
        command.add_argument("--output")
    commands.add_parser("init-env")
    commands.add_parser("serve").add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.command == "init-env":
        init_env()
        return
    if args.command == "serve":
        uvicorn.run("genai_evaluation_platform.api:app", host="127.0.0.1", port=args.port)
        return
    candidate = evaluate_suite(args.suite, threshold=settings.pass_threshold)
    if args.command == "compare":
        baseline = evaluate_suite(
            args.suite, candidate=weak_baseline, threshold=settings.pass_threshold
        )
        print("Baseline pass rate:", baseline.pass_rate)
    print(candidate.model_dump_json(indent=2))
    if args.output:
        write_report(candidate, args.output)
    if not candidate.passed:
        raise SystemExit(1)
