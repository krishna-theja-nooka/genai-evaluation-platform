# Architecture

The platform separates a candidate adapter from evaluation policy. A candidate returns an answer and elapsed time; metrics turn that result and a versioned case into a transparent scorecard.

1. A JSONL suite supplies a prompt, evidence context, expected facts, citations, and latency budget.
2. The runner invokes the selected candidate adapter.
3. Metrics score correctness, citation accuracy, groundedness, safety, and latency.
4. The report aggregates scores and applies a release threshold.

The same suite can compare prompts, models, retrieval configurations, or a remote API without changing evaluation policy.
