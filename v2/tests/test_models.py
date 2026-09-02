from v2.app.models import Issue, RepairState, RunStatus

def test_state_is_bounded_and_typed():
    s=RepairState(issue=Issue(repository="o/r",number=1))
    assert s.status is RunStatus.CREATED
    assert s.budget.max_iterations==3
