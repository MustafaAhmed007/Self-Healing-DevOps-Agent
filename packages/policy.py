from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from packages.models import PatchPolicy


@dataclass(frozen=True)
class DiffStats:
    files: int
    added: int
    deleted: int
    paths: tuple[str, ...]


class PolicyViolation(ValueError):
    pass


class PolicyEngine:
    def __init__(self, policy: PatchPolicy | None = None) -> None:
        self.policy = policy or PatchPolicy()

    def validate_diff(self, diff: str) -> DiffStats:
        paths: list[str] = []
        added = deleted = 0
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                path = line[6:]
                if path != "/dev/null":
                    paths.append(path)
            elif line.startswith("+") and not line.startswith("+++"):
                added += 1
            elif line.startswith("-") and not line.startswith("---"):
                deleted += 1

        unique_paths = tuple(dict.fromkeys(paths))
        reasons: list[str] = []
        if len(unique_paths) > self.policy.max_files_changed:
            reasons.append("maximum changed-file count exceeded")
        if added > self.policy.max_lines_added:
            reasons.append("maximum added-line budget exceeded")
        if deleted > self.policy.max_lines_deleted:
            reasons.append("maximum deleted-line budget exceeded")
        for path in unique_paths:
            if self._protected(path):
                reasons.append(f"protected path modified: {path}")
            if path.endswith((".lock",)) and not self.policy.allow_lockfile_changes:
                reasons.append(f"lockfile modification is blocked: {path}")
        if reasons:
            raise PolicyViolation("; ".join(reasons))
        return DiffStats(len(unique_paths), added, deleted, unique_paths)

    def _protected(self, path: str) -> bool:
        p = PurePosixPath(path)
        for rule in self.policy.protected_paths:
            if rule.endswith("*") and path.startswith(rule[:-1]):
                return True
            if str(p) == rule or path.startswith(rule.rstrip("/") + "/"):
                return True
        if ".github/workflows/" in path and not self.policy.allow_ci_changes:
            return True
        if path.startswith(".env"):
            return True
        return False
