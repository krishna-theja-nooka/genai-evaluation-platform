# Evaluation Guide

Each JSONL record is a stable contract. Keep the prompt, evidence context, expected facts, required citation IDs, and latency budget together. Add benign, adversarial, abstention, and regression cases.

The default suite passes only if every case passes and the aggregate pass rate meets `GENAI_EVAL_PASS_THRESHOLD` (default `0.80`). Production teams should set per-metric floors too; safety and citation accuracy should be 100% for protected workflows.

Token-overlap groundedness is explainable but does not provide semantic reasoning. Add model-assisted judges and human review for production decisions while retaining deterministic checks as a baseline.
