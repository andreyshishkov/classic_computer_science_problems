from typing import TypeVar, Generic, List, Tuple
from graph import Graph
from weighted_edge import WeightedEdge

V = TypeVar('V')


class WeightedGraph(Generic[V], Graph[V]):

    def __init__(self, vertices: List[V] = None) -> None:
        super().__init__(vertices)
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]

    def add_edge_by_indices(self, start: int, end: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(start, end, weight)
        self.add_both_directed_edge(edge)

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        start: int = self._vertices.index(first)
        end: int = self._vertices.index(second)
        self.add_edge_by_indices(start, end, weight)

    def get_neighbors_by_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        distance_tuples: List[Tuple[V, float]] = []
        for edge in self.get_edges_by_vertex_index(index):
            distance_tuples.append((self.get_vertex_by_index(edge.end), edge.weight))
        return distance_tuples

    def __str__(self) -> str:
        desc: str = ''
        for i in range(self.vertex_count):
            desc += f'{self.get_vertex_by_index(i)} -> {self.get_neighbors_by_index_with_weights(i)}\n'
        return desc


if __name__ == '__main__':
    city_graph2: WeightedGraph[str] = WeightedGraph(
        [
            "Seattle", "San Francisco",
            "Los Angeles", "Riverside",
            "Phoenix", "Chicago", "Boston",
            "New York", "Atlanta", "Miami",
            "Dallas", "Houston", "Detroit",
            "Philadelphia", "Washington"
        ]
    )

    city_graph2.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_graph2.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph2.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_graph2.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph2.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_graph2.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph2.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_graph2.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_graph2.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_graph2.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_graph2.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_graph2.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_graph2.add_edge_by_vertices("Dallas", "Houston", 225)
    city_graph2.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_graph2.add_edge_by_vertices("Houston", "Miami", 968)
    city_graph2.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_graph2.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_graph2.add_edge_by_vertices("Atlanta", "Miami", 604)
    city_graph2.add_edge_by_vertices("Miami", "Washington", 923)
    city_graph2.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_graph2.add_edge_by_vertices("Detroit", "Boston", 613)
    city_graph2.add_edge_by_vertices("Detroit", "Washington", 396)
    city_graph2.add_edge_by_vertices("Detroit", "New York", 482)
    city_graph2.add_edge_by_vertices("Boston", "New York", 190)
    city_graph2.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_graph2.add_edge_by_vertices("Philadelphia", "Washington", 123)

    print(city_graph2)
