from __future__ import annotations
from typing import TypedDict
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    StateGraph=END=None

class GraphState(TypedDict, total=False):
    stage: str
    iteration: int
    passed: bool
    failure: str

def build_graph():
    if StateGraph is None: return None
    g=StateGraph(GraphState)
    def reproduce(s): return {"stage":"reproduce"}
    def diagnose(s): return {"stage":"diagnose"}
    def patch(s): return {"stage":"patch"}
    def verify(s): return {"stage":"verify"}
    def route(s): return END if s.get("passed") else "reflect"
    def reflect(s): return {"stage":"reflect","iteration":s.get("iteration",0)+1}
    g.add_node("reproduce",reproduce); g.add_node("diagnose",diagnose); g.add_node("patch",patch); g.add_node("verify",verify); g.add_node("reflect",reflect)
    g.set_entry_point("reproduce"); g.add_edge("reproduce","diagnose"); g.add_edge("diagnose","patch"); g.add_edge("patch","verify"); g.add_conditional_edges("verify",route,{END:END,"reflect":"reflect"}); g.add_edge("reflect","patch")
    return g.compile()
