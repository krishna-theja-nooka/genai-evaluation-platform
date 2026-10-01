from pathlib import Path

from genai_evaluation_platform.runner import evaluate_suite, weak_baseline

SUITE = Path(__file__).parents[1] / "eval" / "sample_suite.jsonl"


def test_sample_suite_passes():
    report = evaluate_suite(SUITE)
    assert report.passed is True
    assert report.pass_rate == 1.0


def test_weak_baseline_fails():
    assert evaluate_suite(SUITE, candidate=weak_baseline).passed is False
