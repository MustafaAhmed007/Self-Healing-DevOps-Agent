from __future__ import annotations

from dataclasses import dataclass
from .models import RiskLevel


@dataclass(frozen=True)
class Route:
    model: str
    strategy: str
    reason: str


class RepairRouter:
    """Safe baseline router; learned promotion can replace the policy only after held-out evaluation."""
    def choose(self, risk: RiskLevel, files: int, failure_complexity: str = "normal") -> Route:
        if risk in {RiskLevel.HIGH, RiskLevel.CRITICAL}:
            return Route("strong-reasoning", "minimal-diff-human-gate", "risk")
        if files > 8 or failure_complexity == "complex":
            return Route("strong-reasoning", "evidence-first", "complexity")
        return Route("fast-default", "evidence-first", "bounded-cost")
