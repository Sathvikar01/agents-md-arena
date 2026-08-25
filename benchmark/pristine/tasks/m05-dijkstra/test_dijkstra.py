from dijkstra import shortest_path

G = {
    "a": [("b", 1), ("c", 4)],
    "b": [("c", 2), ("d", 5)],
    "c": [("d", 1)],
    "d": [],
}


def test_direct_edge():
    assert shortest_path(G, "a", "b") == (1, ["a", "b"])


def test_multi_hop_cheaper_than_direct():
    dist, path = shortest_path(G, "a", "c")
    assert dist == 3 and path[0] == "a" and path[-1] == "c" and len(path) == 3


def test_accumulates_across_hops():
    dist, path = shortest_path(G, "a", "d")
    assert dist == 4
    assert path == ["a", "b", "c", "d"]


def test_start_is_goal():
    assert shortest_path(G, "a", "a") == (0, ["a"])


def test_unreachable():
    H = {"a": [], "b": [("a", 1)]}
    assert shortest_path(H, "b", "a") == (1, ["b", "a"])
    assert shortest_path(H, "a", "b") == (None, [])


def test_unknown_goal_treated_unreachable():
    assert shortest_path(G, "a", "zz") == (None, [])


def test_cycle_does_not_break():
    C = {"x": [("y", 1)], "y": [("x", 1), ("z", 2)], "z": []}
    assert shortest_path(C, "x", "z") == (3, ["x", "y", "z"])
