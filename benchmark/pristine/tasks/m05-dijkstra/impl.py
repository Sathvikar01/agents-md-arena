"""Shortest path with Dijkstra.

graph: {node: [(neighbor, weight), ...]} with non-negative int weights.
shortest_path(graph, start, goal) -> (distance, path list) where path
includes both endpoints. Returns (None, []) if goal is unreachable.
"""
import heapq


def shortest_path(graph: dict, start, goal):
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in graph.get(u, []):
            nd = w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    if goal not in dist:
        return (float("inf"), [])
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return (dist[goal], path[::-1])
