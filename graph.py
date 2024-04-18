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
