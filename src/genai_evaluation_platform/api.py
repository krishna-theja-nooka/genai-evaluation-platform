from __future__ import annotations

import time
from collections import deque

from fastapi import Depends, FastAPI, Header, HTTPException

from .config import settings
from .models import CandidateResult, EvaluateRequest
from .runner import evaluate_case, evaluate_suite

app = FastAPI(title="GenAI Evaluation Platform", version="0.1.0")
_requests: deque[float] = deque()


def authorize(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    now = time.time()
    while _requests and now - _requests[0] > 60:
        _requests.popleft()
    if len(_requests) >= settings.requests_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    _requests.append(now)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "genai-evaluation-platform"}


@app.post("/v1/evaluate", dependencies=[Depends(authorize)])
def evaluate(request: EvaluateRequest):
    return evaluate_case(
        request.case, CandidateResult(answer=request.answer, latency_ms=request.latency_ms)
    )


@app.post("/v1/suites/sample", dependencies=[Depends(authorize)])
def run_sample_suite():
    return evaluate_suite("eval/sample_suite.jsonl", threshold=settings.pass_threshold)
