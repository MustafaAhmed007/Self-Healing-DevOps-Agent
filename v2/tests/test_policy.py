from app.models import Budget, PatchProposal
from app.policy import validate_patch


def test_patch_policy_blocks_workflows():
    errors = validate_patch(PatchProposal(files={".github/workflows/pwn.yml": "x"}), Budget())
    assert errors


def test_patch_policy_allows_small_source_change():
    assert validate_patch(PatchProposal(files={"src/a.py": "print(1)"}), Budget()) == []
