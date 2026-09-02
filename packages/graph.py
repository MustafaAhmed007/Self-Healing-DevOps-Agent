from __future__ import annotations

from packages.models import RepairState


NODES = (
    "issue_analyzer",
    "repository_explorer",
    "bug_reproducer",
    "code_analyst",
    "patch_generator",
    "policy_gate",
    "test_runner",
    "verifier",
    "reflection",
    "pr_generator",
)


def route_after_verification(state: RepairState) -> str:
    if state.verification and state.verification.passed:
        return "pr_generator"
    if state.iteration >= 3:
        return "failed"
    return "reflection"


def build_graph():
    """Build the LangGraph graph when the optional dependency is installed."""
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:
        raise RuntimeError("Install the llm extra to enable LangGraph execution") from exc

    graph = StateGraph(RepairState)
    # Nodes are intentionally registered by the production worker in dependency order.
    # This adapter keeps the state-machine boundary explicit without coupling policy code to LangGraph.
    graph.add_node("issue_analyzer", lambda s: s)
    graph.add_edge(START, "issue_analyzer")
    graph.add_edge("issue_analyzer", END)
    return graph.compile()
