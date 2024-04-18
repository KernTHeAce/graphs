import random
import os
import sys
import pickle


class Vertex:
    number: int  # обозначает номер вершины, её уникальное "Имя"

    def __init__(self, number: int):
        self.number = number
        self.neighbors = []
        self.negativeNeighbors = []
        # self.edges = []
        self.degree = 0
        self.negativeDegree = 0

    # Добавление соседа и увеличение степени
    def add_neighbor(self, neighbor):
        # При возникновении кратных ребер или петель не надо добавлять новых соседей
        if not any(neig == neighbor for neig in self.neighbors):
            self.neighbors.append(neighbor)
        self.degree += 1

    # Добавление отрицательного соседа (для ор графа) и отрицательной степени
    def add_negativeNeighbor(self, neighbor):
        # При возникновении кратных ребер или петель не надо добавлять новых соседей
        if not any(neig == neighbor for neig in self.neighbors):
            self.negativeNeighbors.append(neighbor)
        self.negativeDegree += 1


# Класс Дуга
class Edge:
    def __init__(self, start_vertex, end_vertex, weight=1):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight


# Класс Граф
class Graph:
    def __init__(self, directed=False, weighted=False, allow_loops=False):
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []
        self.directed = directed
        self.weighted = weighted
        self.allow_loops = allow_loops

    # Добавление вершины к графу
    def add_vertex(self, number):
        self.vertices.append(Vertex(number))

    # Добавление дуги к графу
    def add_edge(self, start_vertex, end_vertex, weight=1) -> bool:

        # Проверка на петли
        if not self.allow_loops and start_vertex == end_vertex:
            # raise ValueError("Петли недоступны для этого графа")
            # print("Don`t allow loops. Петли недоступны для этого графа")
            return False

        # Проверка есть ли начальная вершина дуги вообще в графе и её добавление
        if not any(vertex.number == start_vertex for vertex in self.vertices):
            self.add_vertex(start_vertex)

        # Проверка есть ли конечная вершина дуги вообще в графе и её добавление
        if not any(vertex.number == end_vertex for vertex in self.vertices):
            self.add_vertex(end_vertex)

        # Добавление соседей для неор и ор графа
        if not self.directed:
            for vertex in self.vertices:
                if start_vertex == vertex.number:
                    vertex.add_neighbor(end_vertex)
                    # continue Убрал , так как петли делают степени +2
                if end_vertex == vertex.number:
                    vertex.add_neighbor(start_vertex)
        else:
            for vertex in self.vertices:
                # Отриц степень - Сколько входит, Полож степень - сколько выходит
                if start_vertex == vertex.number:
                    vertex.add_neighbor(end_vertex)
                    # continue Убрал, ссылаясь на какой-то форум
                    # "Если граф - ориентированный, то исход петли будет считаться с минусом, а приход - с плюсом. "
                if end_vertex == vertex.number:
                    vertex.add_negativeNeighbor(start_vertex)

        # Наконец-то добавление самой дуги
        if self.weighted:
            self.edges.append(Edge(start_vertex, end_vertex, weight))
        else:
            self.edges.append(Edge(start_vertex, end_vertex))

        return True


# Сгенерировать граф
def GenerateGraph(filename: str) -> Graph:
    gh = Graph()
    with open(filename, "r") as file:
        try:
            # Чтение на 0 (1) — неориентированный (ориентированный)
            #           0 (1) — невзвешенный (взвешенный)
            #           0 (1) — без петель (с петлями)
            line = file.readline().strip().split()
            if line[0] == "1":
                gh.directed = True
            elif line[0] == "0":
                gh.directed = False
            else:
                raise ValueError
            if line[1] == "1":
                gh.weighted = True
            elif line[1] == "0":
                gh.weighted = False
            else:
                raise ValueError
            if line[2] == "1":
                gh.allow_loops = True
            elif line[2] == "0":
                gh.allow_loops = False
            else:
                raise ValueError
            # Чтение диапазона вершин и их создание [Vmin ; Vmax].
            line = list(map(int, file.readline().strip().split()))
            vertexCount = random.randint(line[0], line[1])
            for i in range(1, vertexCount + 1):
                gh.add_vertex(i)
            # Чтение диапазона дуг [Emin ; Emax].
            line = list(map(int, file.readline().strip().split()))
            edgesCount = random.randint(line[0], line[1])
            # Чтение диапазона весов (При необходимости)
            weights = [1 for _ in range(edgesCount)]
            if gh.weighted:
                line = list(map(int, file.readline().strip().split()))
                weights = [random.randint(line[0], line[1]) for _ in range(edgesCount)]
            # Добавление дуг
            i = 0
            while i < edgesCount:
                if gh.add_edge(
                    random.randint(1, vertexCount),
                    random.randint(1, vertexCount),
                    weights[i],
                ):
                    i += 1
            print(
                "Кол-во сгенерированных вершин: ",
                len(gh.vertices),
                "\nКол-во сгенерированных рёбер: ",
                len(gh.edges),
            )
        except (ValueError, IndexError):
            raise SyntaxError("Incorrect file format. Неверный формат файла")
    return gh


def AdjacencyMatrix(graph: Graph, NeedToPrint: bool = False) -> list[list[int]]:
    adjMatrix = [
        [0 for _ in range(len(graph.vertices))] for _ in range(len(graph.vertices))
    ]
    if not graph.directed:
        for edge in graph.edges:
            adjMatrix[edge.start_vertex - 1][edge.end_vertex - 1] += edge.weight
            adjMatrix[edge.end_vertex - 1][edge.start_vertex - 1] += edge.weight
    else:
        for edge in graph.edges:
            adjMatrix[edge.start_vertex - 1][edge.end_vertex - 1] += edge.weight
            # adjMatrix[edge.end_vertex-1][edge.start_vertex-1]+=edge.weight
    if NeedToPrint:
        print(*adjMatrix, sep="\n")
    return adjMatrix


# Степени вершин
def Degrees(graph: Graph, NeedToPrint: bool = False):
    degrees = []
    if graph.directed:
        for vertex in graph.vertices:
            degrees.append([vertex.degree, vertex.negativeDegree])
    else:
        for vertex in graph.vertices:
            degrees.append(vertex.degree)
    if NeedToPrint:
        for index, vertex in enumerate(graph.vertices):
            print(f"{vertex.number} : {degrees[index]}")
    return degrees


# Параллельные ребра
def MultipleEdge(graph: Graph, NeedToPrint: bool = False):
    parallel_edges = {}
    vertex_pair = None
    for edge in graph.edges:
        if not graph.directed:
            vertex_pair = (
                (edge.start_vertex, edge.end_vertex)
                if edge.start_vertex <= edge.end_vertex
                else (edge.end_vertex, edge.start_vertex)
            )
        else:
            vertex_pair = (edge.start_vertex, edge.end_vertex)
        if vertex_pair in parallel_edges:
            parallel_edges[vertex_pair][0] += 1
            parallel_edges[vertex_pair][1].append(edge.weight)
        else:
            parallel_edges[vertex_pair] = [1, [edge.weight]]
    result = ""
    for vertices, (count, weights) in parallel_edges.items():
        if count > 1:
            result += f"({vertices[0]}-{vertices[1]}) - {count}: {', '.join(map(str, weights))}\n"
    if NeedToPrint:
        print(result)
    return result


# Наличие петель:
def IsHaveLoops(graph: Graph, NeedToPrint: bool = False):
    result = ""
    ishaveloops = False
    for edge in graph.edges:
        if edge.start_vertex == edge.end_vertex:
            ishaveloops = True
            result += f"{edge.start_vertex}-{edge.end_vertex} : {edge.weight}\n"
    if NeedToPrint:
        print(result)
    return ishaveloops


# Список упорядоченных пар смежных вершин (используется при задании графа списком).
def PairsOfAdjacentVertices(graph: Graph, NeedToPrint: bool = False):
    result = ""
    for vert in graph.vertices:
        result += f"{vert.number}: {vert.neighbors}\n"
    if NeedToPrint:
        print(result)
    return result


# Матрицу инцидентности ребер
def IncidenceMatrix(graph: Graph, NeedToPrint: bool = False):
    matrix = [[0 for _ in range(len(graph.edges))] for _ in range(len(graph.vertices))]
    if graph.directed:
        for index, edge in enumerate(graph.edges):
            if edge.start_vertex == edge.end_vertex:
                matrix[edge.start_vertex - 1][index] = 2
                continue
            matrix[edge.start_vertex - 1][index] = 1
            matrix[edge.end_vertex - 1][index] = -1
    else:
        for index, edge in enumerate(graph.edges):
            if edge.start_vertex == edge.end_vertex:
                matrix[edge.start_vertex - 1][index] = 2
                continue
            matrix[edge.start_vertex - 1][index] = 1
            matrix[edge.end_vertex - 1][index] = 1
    if NeedToPrint:
        print(*matrix, sep="\n")


if __name__ == "__main__":
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # file_path = os.path.join(dir_path,"settings.txt")
    # gh = GenerateGraph(file_path)
    with open("data.pkl", "rb") as inp:
        gh = pickle.load(inp)
    print("Матрица смежности вершин")
    AdjacencyMatrix(gh, True)
    print("\nПараллельные ребра")
    MultipleEdge(gh, True)
    print("Наличие Петель")
    IsHaveLoops(gh, True)
    print("Степени")
    Degrees(gh, True)
    print("\nСписок упорядоченных пар смежных вершин ")
    PairsOfAdjacentVertices(gh, True)
    print("Матрица инцидентности")
    IncidenceMatrix(gh, True)

    with open("data.pkl", "wb") as outp:
        pickle.dump(gh, outp, pickle.HIGHEST_PROTOCOL)
