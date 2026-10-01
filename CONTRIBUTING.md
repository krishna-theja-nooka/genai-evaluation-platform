# Contributing

Keep evaluation cases deterministic and free of real customer data. Every new metric needs a unit test and every new evaluation case needs an expected outcome.

Run before opening a pull request:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
python -m genai_evaluation_platform evaluate --suite eval/sample_suite.jsonl
```
