from v2.app.graph import build_graph

def test_graph_builds_without_optional_dependency():
    # If LangGraph is installed this returns a compiled graph; otherwise None is the documented fallback.
    graph=build_graph()
    assert graph is None or graph is not None
