import pickle
import sys

from graph import Graph, Vertex, Edge


def dijkstra(graph, start_vertex, flag=True):
    dist = {vertex.number: sys.maxsize for vertex in graph.vertices}
    dist[start_vertex] = 0

    if not flag:
        for i in range(len(graph.edges)):
            graph.edges[i].weight = 100_000 - graph.edges[i].weight

    visited = set()
    previous = {vertex.number: None for vertex in graph.vertices}

    while len(visited) < len(graph.vertices):
        min_dist = sys.maxsize
        u = None

        for vertex in graph.vertices:
            if vertex.number not in visited and dist[vertex.number] < min_dist:
                min_dist = dist[vertex.number]
                u = vertex.number

        if u is None:
            break

        visited.add(u)

        for edge in graph.edges:
            if edge.start_vertex == u:
                v = edge.end_vertex
                alt = dist[u] + edge.weight

                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u

    return dist, previous


# Функция для восстановления пути
def reconstruct_path(previous, start_vertex, end_vertex):
    path = []
    current_vertex = end_vertex
    while current_vertex is not None:
        path.insert(0, current_vertex)
        current_vertex = previous[current_vertex]
    if path[0] == start_vertex:
        return path
    else:
        return None


with open("data.pkl", "rb") as inp:
    gh = pickle.load(inp)

start_vertex = gh.vertices[0].number
distances, previous = dijkstra(
    gh,
    start_vertex,
)
end_vertex = 4  # Пример вершины, к которой ищется путь
path = reconstruct_path(previous, start_vertex, end_vertex)

if path is not None:
    print(
        "Shortest path from vertex", start_vertex, "to vertex", end_vertex, "is:", path
    )
    print(f"Len: {distances[end_vertex]}")
    distances, previous = dijkstra(gh, start_vertex, False)
    path = reconstruct_path(previous, start_vertex, end_vertex)
    print(
        "Longest path from vertex", start_vertex, "to vertex", end_vertex, "is:", path
    )
    print(f"Len: {100_000 - (distances[end_vertex] % 100_000)}")
else:
    print("There is no path from vertex", start_vertex, "to vertex", end_vertex)
