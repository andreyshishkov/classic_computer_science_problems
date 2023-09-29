from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint


Point = TypeVar('Point', bound=DataPoint)


def z_scores(original: Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)

    if std == 0:
        return [0] * len(original)

    return [(x - avg) / std for x in original]


@dataclass
class Cluster:
    points: List[Point]
    centroid: DataPoint


class KMeans(Generic[Point]):

    def __init__(self, k: int, points: List[Point]) -> None:
        if k < 1:
            raise ValueError('K must be >= 1')
        self._points: List[Point] = points
        self._z_score_normalize()

        self._clusters: List[Cluster] = []

        for _ in range(k):
            rand_point: DataPoint = self._get_random_point()
            cluster: Cluster = Cluster([], rand_point)
            self._clusters.append(cluster)

    def get_clusters(self):
        return self._clusters

    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]

    def _dimension_slices(self, dimension: int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]

    def _z_score_normalize(self) -> None:
        z_scored: List[List[float]] = [[] for _ in range(len(self._points))]

        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimension_slices(dimension)
            for index, z_score in enumerate(z_scores(dimension_slice)):
                z_scored[index].append(z_score)

        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(z_scored[i])

    def _get_random_point(self) -> DataPoint:
        rand_dimensions: List[float] = []
        for dimension in range(self._points[0].num_dimensions):
            values: List[float] = self._dimension_slices(dimension)
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
        return DataPoint(rand_dimensions)

    def assign_clusters(self) -> None:
        for point in self._points:
            closest: DataPoint = min(self._centroids, key=partial(DataPoint.distance, point))
            idx: int = self._centroids.index(closest)
            cluster: Cluster = self._clusters[idx]
            cluster.points.append(point)

    def generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) == 0:
                continue
            means: List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [p.dimensions[dimension] for p in cluster.points]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)

    def run(self, max_iterations: int = 100) -> None:
        for iteration in range(max_iterations):
            for cluster in self._clusters:
                cluster.points.clear()
            self.assign_clusters()
            old_centroids: List[DataPoint] = deepcopy(self._centroids)
            self.generate_centroids()

            if old_centroids == self._centroids:
                print(f'Converaged after {iteration} iterations')
                return


if __name__ == "__main__":
    point1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    point2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    point3: DataPoint = DataPoint([3.0, 1.5, 2.5])
    kmeans_test: KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    kmeans_test.run()
    test_clusters: List[Cluster] = kmeans_test.get_clusters()
    for index, cluster in enumerate(test_clusters):
        print(f"Cluster {index}: {cluster.points}")