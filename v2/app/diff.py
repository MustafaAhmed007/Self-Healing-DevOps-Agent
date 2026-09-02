from __future__ import annotations

import difflib
from pathlib import Path
from .models import Budget, PatchProposal
from .policy import validate_patch


def unified_diff(root: Path, files: dict[str, str]) -> str:
    chunks: list[str] = []
    for name, new_content in files.items():
        target = root / name
        old = target.read_text(errors="replace") if target.exists() else ""
        chunks.extend(difflib.unified_diff(old.splitlines(True), new_content.splitlines(True), fromfile=f"a/{name}", tofile=f"b/{name}"))
    return "".join(chunks)


def apply_proposal(root: Path, proposal: PatchProposal, budget: Budget) -> str:
    errors = validate_patch(proposal, budget)
    if errors:
        raise PermissionError("; ".join(errors))
    diff = unified_diff(root, proposal.files)
    for name, content in proposal.files.items():
        target = (root / name).resolve()
        if root.resolve() not in target.parents:
            raise PermissionError(f"patch escapes workspace: {name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    return diff
