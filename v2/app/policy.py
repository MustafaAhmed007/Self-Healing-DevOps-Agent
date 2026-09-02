from __future__ import annotations

import shlex
from pathlib import Path
from .models import Budget, PatchProposal

PROTECTED_PREFIXES = (".git/", ".github/workflows/", ".github/actions/")
PROTECTED_FILES = {".env", ".env.local", ".env.production"}
BLOCKED_EXT = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
BLOCKED_COMMANDS = {"sudo", "su", "mount", "umount", "nsenter", "unshare", "docker", "podman", "kubectl"}
BLOCKED_ARGS = {"--privileged", "--network=host", "--pid=host", "--ipc=host", "-v /:/host"}


def validate_patch(patch: PatchProposal, budget: Budget) -> list[str]:
    errors: list[str] = []
    if len(patch.files) > budget.max_patch_files:
        errors.append("patch file limit exceeded")
    if sum(len(v.splitlines()) for v in patch.files.values()) > budget.max_patch_lines:
        errors.append("patch line limit exceeded")
    for raw in patch.files:
        p = Path(raw)
        normalized = raw.replace("\\", "/")
        if p.is_absolute() or ".." in p.parts:
            errors.append(f"unsafe path: {raw}")
        if normalized in PROTECTED_FILES or normalized.startswith(PROTECTED_PREFIXES):
            errors.append(f"protected path: {raw}")
        if p.suffix.lower() in BLOCKED_EXT:
            errors.append(f"sensitive extension: {raw}")
    return errors


def validate_command(argv: list[str]) -> None:
    if not argv or len(argv) > 32:
        raise PermissionError("invalid command")
    for token in argv:
        if token in BLOCKED_COMMANDS or token in BLOCKED_ARGS:
            raise PermissionError(f"blocked command argument: {token}")
        if any(x in token for x in ("/proc/", "/sys/", "/dev/", "$(", "`", ";", "&&", "||")):
            raise PermissionError("potential shell escape or host path blocked")


def command_string(argv: list[str]) -> str:
    validate_command(argv)
    return shlex.join(argv)
