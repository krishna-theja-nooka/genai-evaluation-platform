from __future__ import annotations

import json
import time
from pathlib import Path

from .metrics import score_case
from .models import CandidateResult, CaseResult, EvaluationCase, SuiteReport


def load_suite(path: str | Path) -> list[EvaluationCase]:
    return [
        EvaluationCase.model_validate_json(line)
        for line in Path(path).read_text().splitlines()
        if line
    ]


def deterministic_candidate(case: EvaluationCase) -> CandidateResult:
    started = time.perf_counter()
    answer = case.response or "I don't have enough evidence to answer that question."
    return CandidateResult(
        answer=answer, latency_ms=round((time.perf_counter() - started) * 1000, 3)
    )


def weak_baseline(case: EvaluationCase) -> CandidateResult:
    return CandidateResult(answer="I am not sure.", latency_ms=2.0)


def evaluate_case(case: EvaluationCase, result: CandidateResult) -> CaseResult:
    scores, failures = score_case(case, result)
    return CaseResult(
        case_id=case.id,
        passed=not failures,
        scores=scores,
        failures=failures,
        latency_ms=result.latency_ms,
    )


def evaluate_suite(
    suite_path: str | Path, candidate=deterministic_candidate, threshold: float = 0.80
) -> SuiteReport:
    cases = [evaluate_case(case, candidate(case)) for case in load_suite(suite_path)]
    total = len(cases) or 1
    pass_rate = sum(case.passed for case in cases) / total
    metric_names = ("correctness", "citation_accuracy", "groundedness", "safety", "latency")
    metrics = {
        name: round(sum(case.scores[name] for case in cases) / total, 3) for name in metric_names
    }
    sorted_latency = sorted(case.latency_ms for case in cases)
    p95_index = min(len(sorted_latency) - 1, max(0, int(len(sorted_latency) * 0.95)))
    return SuiteReport(
        suite=Path(suite_path).stem,
        passed=pass_rate >= threshold and all(case.passed for case in cases),
        pass_rate=round(pass_rate, 3),
        metrics=metrics,
        latency_ms_p95=sorted_latency[p95_index] if sorted_latency else 0,
        cases=cases,
    )


def write_report(report: SuiteReport, output: str | Path) -> None:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report.model_dump(), indent=2) + "\n")
