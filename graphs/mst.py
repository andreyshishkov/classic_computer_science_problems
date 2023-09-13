from typing import TypeVar, List, Optional
from weighted_edge import WeightedEdge
from weighted_graph import WeightedGraph
from priority_queue import PriorityQueue

V = TypeVar('V')
WeightedPath = List[WeightedEdge]


def get_total_weight(weight_path: WeightedPath) -> float:
    return sum(edge.weight for edge in weight_path)


def visit(index: int, visited_vertices: List[bool], pq: PriorityQueue, wg: WeightedGraph) -> None:
    visited_vertices[index] = True
    for edge in wg.get_edges_by_vertex_index(index):
        if not visited_vertices[edge.end]:
            pq.push(edge)


def mst(weighted_graph: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (weighted_graph.vertex_count - 1) or start < 0:
        return None

    result: WeightedPath = []
    priority_queue: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: List[bool] = [False] * weighted_graph.vertex_count

    visit(start, visited, priority_queue, weighted_graph)

    while not priority_queue.empty:
        edge: WeightedEdge = priority_queue.pop()
        if visited[edge.end]:
            continue

        result.append(edge)
        visit(edge.end,  visited, priority_queue, weighted_graph)

    return result


def print_weighted_path(weighted_graph: WeightedGraph, weighted_path: WeightedPath) -> None:
    for edge in weighted_path:
        start: V = weighted_graph.get_vertex_by_index(edge.start)
        end: V = weighted_graph.get_vertex_by_index(edge.end)
        print(f'{start} {edge.weight} -> {end}')
    print('-----------------------')
    print(f'Total weight: {get_total_weight(weighted_path)}')


if __name__ == '__main__':
    city_graph2: WeightedGraph[str] = WeightedGraph(
        [
            "Seattle", "San Francisco",
            "Los Angeles", "Riverside", "Phoenix",
            "Chicago", "Boston",
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
    result: Optional[WeightedPath] = mst(city_graph2)
    if result is None:
        print("No solution found!")
    else:
        print_weighted_path(city_graph2, result)
