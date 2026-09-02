from __future__ import annotations

from typing import TypedDict

try:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import END, StateGraph
except ImportError:
    MemorySaver = StateGraph = END = None


class GraphState(TypedDict, total=False):
    stage: str
    iteration: int
    passed: bool
    failure: str


def build_graph(checkpointer=None, max_iterations: int = 3):
    if StateGraph is None:
        return None
    graph = StateGraph(GraphState)

    def reproduce(state):
        return {"stage": "reproduce"}

    def diagnose(state):
        return {"stage": "diagnose"}

    def patch(state):
        return {"stage": "patch"}

    def verify(state):
        return {"stage": "verify"}

    def reflect(state):
        return {"stage": "reflect", "iteration": state.get("iteration", 0) + 1}

    def route(state):
        if state.get("passed"):
            return END
        if state.get("iteration", 0) >= max_iterations:
            return END
        return "reflect"

    for name, fn in (("reproduce", reproduce), ("diagnose", diagnose), ("patch", patch), ("verify", verify), ("reflect", reflect)):
        graph.add_node(name, fn)
    graph.set_entry_point("reproduce")
    graph.add_edge("reproduce", "diagnose")
    graph.add_edge("diagnose", "patch")
    graph.add_edge("patch", "verify")
    graph.add_conditional_edges("verify", route, {END: END, "reflect": "reflect"})
    graph.add_edge("reflect", "diagnose")
    return graph.compile(checkpointer=checkpointer or MemorySaver())
