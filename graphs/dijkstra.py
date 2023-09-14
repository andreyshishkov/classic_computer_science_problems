from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass
from mst import WeightedPath, print_weighted_path
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V')


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(weighted_graph: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = weighted_graph.get_index_of_vertex(root)

    distances: List[Optional[float]] = [None] * weighted_graph.vertex_count
    distances[first] = 0

    path_dict: Dict[int, WeightedEdge] = {}

    priority_queue: PriorityQueue[DijkstraNode] = PriorityQueue()
    priority_queue.push(DijkstraNode(first, 0))

    while not priority_queue.empty:
        current_vertex_index: int = priority_queue.pop().vertex
        dist_to_cur_ver: float = distances[current_vertex_index]

        for edge in weighted_graph.get_edges_by_vertex_index(current_vertex_index):
            dist_to_end: float = distances[edge.end]

            if dist_to_end is None or dist_to_end > dist_to_cur_ver + edge.weight:
                distances[edge.end] = dist_to_cur_ver + edge.weight

                path_dict[edge.end] = edge
                priority_queue.push(DijkstraNode(edge.end, edge.weight + dist_to_cur_ver))

    return distances, path_dict


def get_distance_array_to_vertex_dict(
        weighted_graph: WeightedGraph[V],
        distances: List[Optional[float]]
) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    for i, dist_to_vertex in enumerate(distances):
        distance_dict[weighted_graph.get_vertex_by_index(i)] = dist_to_vertex
    return distance_dict


def path_dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []

    edge_path: WeightedPath = []
    edge: WeightedEdge = path_dict[end]
    edge_path.append(edge)

    while edge.start != start:
        edge = path_dict[edge.start]
        edge_path.append(edge)

    return list(reversed(edge_path))


if __name__ == '__main__':
    city_graph2: WeightedGraph[str] = WeightedGraph(
        [
            "Seattle", "San Francisco",
            "Los Angeles", "Riverside",
            "Phoenix", "Chicago",
            "Boston", "New York",
            "Atlanta", "Miami",
            "Dallas", "Houston",
            "Detroit", "Philadelphia", "Washington"
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
    distances, path_dict = dijkstra(city_graph2, "Los Angeles")
    name_distance: Dict[str, Optional[int]] = get_distance_array_to_vertex_dict(city_graph2, distances)
    print("Distances from Los Angeles:")
    for key, value in name_distance.items():
        print(f"{key} : {value}")
    print("")  # blank line
    print("Shortest path from Los Angeles to Boston:")
    path: WeightedPath = path_dict_to_path(
        city_graph2.get_index_of_vertex("Los Angeles"),
        city_graph2.get_index_of_vertex("Boston"), path_dict)
    print_weighted_path(city_graph2, path)
