from pathlib import Path
import pytest
from app.diff import apply_proposal
from app.models import Budget, PatchProposal


def test_apply_proposal_creates_file(tmp_path: Path):
    proposal = PatchProposal(files={"app.py": "print('ok')\n"})
    diff = apply_proposal(tmp_path, proposal, Budget())
    assert (tmp_path / "app.py").read_text() == "print('ok')\n"
    assert "+++ b/app.py" in diff


def test_apply_proposal_blocks_traversal(tmp_path: Path):
    proposal = PatchProposal(files={"../escape.py": "bad"})
    with pytest.raises(PermissionError):
        apply_proposal(tmp_path, proposal, Budget())
