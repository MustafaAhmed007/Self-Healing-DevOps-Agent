from pathlib import Path

from packages.evaluation import EvalCase, summarize


def test_summary_empty():
    assert summarize({} if False else [])['cases'] == 0


def test_summary_rate():
    from packages.evaluation import EvalResult
    results = [EvalResult('a', True, 10), EvalResult('b', False, 20)]
    assert summarize(results)['issue_resolution_rate'] == 0.5


def test_case_fixture_exists():
    assert Path('evals/devops/bug_001.json').exists()
