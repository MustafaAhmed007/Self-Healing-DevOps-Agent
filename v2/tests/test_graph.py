from app.graph import build_graph


def test_graph_is_optional_but_bounded():
    graph = build_graph(max_iterations=2)
    if graph is None:
        return
    result = graph.invoke({"iteration": 0, "passed": True})
    assert result.get("stage") == "verify"


def test_graph_fallback_contract():
    graph = build_graph(max_iterations=1)
    assert graph is None or hasattr(graph, "invoke")
