import heapq


def shortest_path(graph: dict, start, goal):
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    if goal not in dist:
        return (None, [])
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return (dist[goal], path[::-1])
