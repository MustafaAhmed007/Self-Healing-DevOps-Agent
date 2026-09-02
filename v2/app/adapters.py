from __future__ import annotations

from pathlib import Path


ADAPTERS = {
    "python": ["python", "-m", "pytest", "-q"],
    "node": ["npm", "test", "--", "--runInBand"],
    "go": ["go", "test", "./..."],
    "rust": ["cargo", "test", "--locked"],
    "java": ["./gradlew", "test"],
}


def detect_language(root: Path) -> str:
    markers = [("pyproject.toml", "python"), ("package.json", "node"), ("go.mod", "go"), ("Cargo.toml", "rust"), ("pom.xml", "java")]
    for filename, language in markers:
        if (root / filename).exists():
            return language
    return "unknown"


def default_test_command(root: Path) -> list[str]:
    language = detect_language(root)
    if language not in ADAPTERS:
        raise RuntimeError("no safe test adapter detected")
    return ADAPTERS[language].copy()
