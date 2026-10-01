from genai_evaluation_platform.api import evaluate, health
from genai_evaluation_platform.models import EvaluateRequest


def test_health():
    assert health()["status"] == "ok"


def test_evaluate_endpoint():
    response = evaluate(
        EvaluateRequest(
            case={"id": "one", "prompt": "What?", "expected_facts": ["hello"]},
            answer="hello",
            latency_ms=1,
        )
    )
    assert response.passed is True
