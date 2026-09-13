from pathlib import Path

from app.research import MultiAspectResearch


def test_local_research_is_deterministic(tmp_path: Path):
    (tmp_path / "README.md").write_text("verification and security evidence for repair")
    (tmp_path / "irrelevant.bin").write_bytes(b"verification")
    results = MultiAspectResearch().gather("repair verification", repo=tmp_path, aspects=["verification"])
    assert results
    assert results[0].source == "local"
    assert results[0].title == "README.md"


def test_private_and_malformed_urls_are_rejected():
    research = MultiAspectResearch(timeout=1)
    assert research._url("http://127.0.0.1:8000/internal") is None
    assert research._url("http://localhost/internal") is None
    assert research._url("file:///etc/passwd") is None
    assert research._url("https://user:pass@example.com/") is None


def test_context_is_bounded():
    research = MultiAspectResearch(max_chars=100)
    results = research.gather("evidence", repo=Path("."))
    context = research.context(results)
    assert len(context) <= 100
