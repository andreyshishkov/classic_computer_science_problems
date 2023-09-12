import sys
from typing import TypeVar, Generic, List, Optional
from edge import Edge

V = TypeVar('V')


class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = None) -> None:
        self._vertices: List[V] = vertices if vertices is not None else []
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    def __str__(self):
        desc: str = ''
        for i in range(self.vertex_count):
            desc += f'{self.get_vertex_by_index(i)} -> {self.get_neighbors_of_vertex_by_index(i)}\n'
        return desc

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(len(edges_per_vert) for edges_per_vert in self._edges)

    def add_vertex(self, vertex: V) -> None:
        self._vertices.append(vertex)
        self._edges.append([])

    @property
    def last_vertex_index(self) -> int:
        return self.vertex_count - 1

    def add_both_directed_edge(self, edge: Edge) -> None:
        self._edges[edge.start].append(edge)
        self._edges[edge.end].append(edge.reversed())

    def add_edge_by_indices(self, start: int, end: int) -> None:
        edge: Edge = Edge(start, end)
        self.add_both_directed_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V) -> None:
        start: int = self._vertices.index(first)
        finish: int = self._vertices.index(second)
        self.add_edge_by_indices(start, finish)

    def get_vertex_by_index(self, index: int) -> V:
        return self._vertices[index]

    def get_index_of_vertex(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    def get_neighbors_of_vertex_by_index(self, index: int) -> List[V]:
        return [self.get_vertex_by_index(edge.end) for edge in self._edges[index]]

    def get_neighbors_of_vertex(self, vertex: V) -> List[V]:
        vertex_index: int = self.get_index_of_vertex(vertex)
        return self.get_neighbors_of_vertex_by_index(vertex_index)

    def get_edges_by_vertex_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    def get_edges_of_vertex(self, vertex: V) -> List[Edge]:
        index = self._vertices.index(vertex)
        return self.get_edges_by_vertex_index(index)


if __name__ == "__main__":
    city_graph: Graph[str] = Graph(
     [
         "Seattle", "San Francisco", "Los Angeles", "Riverside",
         "Phoenix", "Chicago", "Boston", "New York",
         "Atlanta", "Miami", "Dallas", "Houston", "Detroit",
         "Philadelphia", "Washington"
     ]
    )
    city_graph.add_edge_by_vertices("Seattle", "Chicago")
    city_graph.add_edge_by_vertices("Seattle", "San Francisco")
    city_graph.add_edge_by_vertices("San Francisco", "Riverside")
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles")
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside")
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Chicago")
    city_graph.add_edge_by_vertices("Phoenix", "Dallas")
    city_graph.add_edge_by_vertices("Phoenix", "Houston")
    city_graph.add_edge_by_vertices("Dallas", "Chicago")
    city_graph.add_edge_by_vertices("Dallas", "Atlanta")
    city_graph.add_edge_by_vertices("Dallas", "Houston")
    city_graph.add_edge_by_vertices("Houston", "Atlanta")
    city_graph.add_edge_by_vertices("Houston", "Miami")
    city_graph.add_edge_by_vertices("Atlanta", "Chicago")
    city_graph.add_edge_by_vertices("Atlanta", "Washington")
    city_graph.add_edge_by_vertices("Atlanta", "Miami")
    city_graph.add_edge_by_vertices("Miami", "Washington")
    city_graph.add_edge_by_vertices("Chicago", "Detroit")
    city_graph.add_edge_by_vertices("Detroit", "Boston")
    city_graph.add_edge_by_vertices("Detroit", "Washington")
    city_graph.add_edge_by_vertices("Detroit", "New York")
    city_graph.add_edge_by_vertices("Boston", "New York")
    city_graph.add_edge_by_vertices("New York", "Philadelphia")
    city_graph.add_edge_by_vertices("Philadelphia", "Washington")
    print(city_graph)

    sys.path.insert(0, '..')
    from generic_search.generic_search import bfs, Node, node_to_path

    bfs_result: Optional[Node[V]] = bfs('Boston', lambda x: x == "Miami", city_graph.get_neighbors_of_vertex)

    if bfs_result is None:
        print("No solution found using breadth-first search!")
    else:
        path:List[V] = node_to_path(bfs_result)
        print("Path from Boston to Miami:")
        print(path)


        

