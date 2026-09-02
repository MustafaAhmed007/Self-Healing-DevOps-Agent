from pathlib import Path
from .models import Budget, PatchProposal

PROTECTED = {".env", ".git/config", ".github/workflows"}
BLOCKED_EXT = {".pem", ".key", ".p12", ".pfx"}

def validate_patch(patch: PatchProposal, budget: Budget) -> list[str]:
    errors=[]
    if len(patch.files) > budget.max_patch_files: errors.append("patch file limit exceeded")
    added=sum(len(v.splitlines()) for v in patch.files.values())
    if added > budget.max_patch_lines: errors.append("patch line limit exceeded")
    for raw in patch.files:
        p=Path(raw)
        if raw in PROTECTED or raw.startswith(".github/workflows/"):
            errors.append(f"protected path: {raw}")
        if p.suffix.lower() in BLOCKED_EXT:
            errors.append(f"sensitive extension: {raw}")
        if ".." in p.parts or p.is_absolute(): errors.append(f"unsafe path: {raw}")
    return errors

def validate_command(argv: list[str]) -> None:
    if not argv or any(x in argv for x in ("--privileged", "--network=host")):
        raise PermissionError("blocked command")
