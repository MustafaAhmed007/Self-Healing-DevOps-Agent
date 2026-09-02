from app.models import Issue, RepairState, RunStatus


def test_state_is_bounded_and_typed():
    state = RepairState(issue=Issue(repository="o/r", number=1))
    assert state.status is RunStatus.CREATED
    assert state.budget.max_iterations == 3
