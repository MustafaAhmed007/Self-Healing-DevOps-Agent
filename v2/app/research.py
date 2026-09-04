from __future__ import annotations

import json
import os
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class ResearchResult:
    source: str
    title: str
    content: str
    confidence: str


class MultiAspectResearch:
    """Evidence-first research with optional cloud search and deterministic fallbacks.

    Priority: configured cloud endpoint -> direct URLs -> local repository evidence.
    Cloud research is never required for a repair run to remain functional.
    """

    def __init__(self, cloud_url: str | None = None, timeout: int = 15, max_chars: int = 12000):
        self.cloud_url = cloud_url or os.getenv("SHDA_RESEARCH_URL")
        self.timeout = timeout
        self.max_chars = max_chars

    def gather(
        self,
        question: str,
        repo: Path | None = None,
        urls: list[str] | None = None,
        aspects: list[str] | None = None,
    ) -> list[ResearchResult]:
        aspects = aspects or ["problem", "implementation", "verification", "security"]
        results: list[ResearchResult] = []
        if self.cloud_url:
            results.extend(self._cloud(question, aspects))
        for url in urls or []:
            result = self._url(url)
            if result:
                results.append(result)
        if repo:
            results.extend(self._local(repo, question, aspects))
        return self._dedupe(results)

    def context(self, results: list[ResearchResult]) -> str:
        if not results:
            return "No external research source was available; rely on repository evidence."
        chunks = [f"[{r.source}] {r.title}\n{r.content}" for r in results]
        return "\n\n".join(chunks)[-self.max_chars :]

    def _cloud(self, question: str, aspects: list[str]) -> list[ResearchResult]:
        payload = json.dumps({"query": question, "aspects": aspects}).encode()
        request = urllib.request.Request(
            self.cloud_url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8", errors="replace"))
            items = data.get("results", data if isinstance(data, list) else [])
            return [
                ResearchResult(
                    source="cloud",
                    title=str(item.get("title", "cloud result")),
                    content=str(item.get("content", ""))[: self.max_chars],
                    confidence="external",
                )
                for item in items[:8]
                if item.get("content")
            ]
        except Exception:
            return []

    def _url(self, url: str) -> ResearchResult | None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return None
        request = urllib.request.Request(url, headers={"User-Agent": "SHDA-research/0.3"})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read(self.max_chars * 2).decode("utf-8", errors="replace")
            text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", body, flags=re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            return ResearchResult(source="direct-url", title=url, content=text[: self.max_chars], confidence="external")
        except Exception:
            return None

    def _local(self, repo: Path, question: str, aspects: list[str]) -> list[ResearchResult]:
        terms = set(re.findall(r"[a-zA-Z0-9_/-]{3,}", question.lower()))
        terms.update(a.lower() for a in aspects)
        candidates = [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]
        preferred = [p for p in candidates if p.suffix.lower() in {".md", ".rst", ".txt", ".py", ".toml", ".yaml", ".yml"}]
        results: list[ResearchResult] = []
        for path in preferred[:80]:
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            score = sum(1 for term in terms if term in text.lower())
            if score:
                results.append(ResearchResult("local", str(path.relative_to(repo)), text[:4000], "repository"))
        return sorted(results, key=lambda r: terms.intersection(set(re.findall(r"\w+", r.content.lower()))).__len__(), reverse=True)[:8]

    @staticmethod
    def _dedupe(results: list[ResearchResult]) -> list[ResearchResult]:
        seen: set[tuple[str, str]] = set()
        unique = []
        for result in results:
            key = (result.source, result.title)
            if key not in seen:
                seen.add(key)
                unique.append(result)
        return unique
