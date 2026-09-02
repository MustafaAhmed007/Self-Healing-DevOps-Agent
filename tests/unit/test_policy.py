from packages.models import PatchPolicy
from packages.policy import PolicyEngine, PolicyViolation


def test_small_safe_diff_passes():
    diff = "diff --git a/src/a.py b/src/a.py\n+++ b/src/a.py\n@@\n+return 1\n"
    stats = PolicyEngine().validate_diff(diff)
    assert stats.files == 1
    assert stats.added == 1


def test_workflow_change_is_blocked():
    diff = "+++ b/.github/workflows/ci.yml\n+echo unsafe\n"
    try:
        PolicyEngine().validate_diff(diff)
    except PolicyViolation as exc:
        assert "protected path" in str(exc)
    else:
        raise AssertionError("workflow change should be blocked")


def test_custom_policy_can_raise_limits():
    engine = PolicyEngine(PatchPolicy(max_files_changed=1))
    diff = "+++ b/a.py\n+x\n+++ b/b.py\n+y\n"
    try:
        engine.validate_diff(diff)
    except PolicyViolation:
        pass
    else:
        raise AssertionError("file limit should be enforced")
