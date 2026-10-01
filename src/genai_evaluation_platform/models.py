from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluationCase(BaseModel):
    id: str
    prompt: str
    context: str = ""
    expected_facts: list[str] = Field(default_factory=list)
    required_citations: list[str] = Field(default_factory=list)
    max_latency_ms: float = 1000
    response: str | None = None


class CandidateResult(BaseModel):
    answer: str
    latency_ms: float


class CaseResult(BaseModel):
    case_id: str
    passed: bool
    scores: dict[str, float]
    failures: list[str]
    latency_ms: float


class SuiteReport(BaseModel):
    suite: str
    passed: bool
    pass_rate: float
    metrics: dict[str, float]
    latency_ms_p95: float
    cases: list[CaseResult]


class EvaluateRequest(BaseModel):
    case: EvaluationCase
    answer: str
    latency_ms: float = 0
