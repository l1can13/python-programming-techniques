from typing import Union, Dict, List
import numpy as np
import random


def distance(left: np.ndarray, right: np.ndarray) -> float:
    return np.linalg.norm(right - left)


class KMeans:
    def __init__(self, n_clusters: int):
        self._n_clusters: int = n_clusters
        self._data: Union[np.ndarray, None] = None
        self._clusters_centers: Union[List[np.ndarray], None] = None
        self._clusters: Union[List[List[int]], None] = None
        self._distance_threshold: float = 0.01

    @property
    def n_clusters(self) -> int:
        return self._n_clusters

    @property
    def n_samples(self) -> int:
        return 0 if self._data is None else self._data.shape[0]

    @property
    def n_features(self) -> int:
        return 0 if self._data is None else self._data.shape[1]

    def _create_start_clusters_centers(self):
        if self._clusters is None:
            self._clusters = []
            self._clusters_centers = []

        self._clusters.clear()
        self._clusters_centers.clear()

        clusters_ids = set()  # проверка, что мы не воткнём две одинаковые точки, как центр кластера

        while len(self._clusters) != self.n_clusters:
            cluster_center_index = random.randint(0, self.n_samples - 1)
            if cluster_center_index in clusters_ids:
                continue
            clusters_ids.update({cluster_center_index})
            self._clusters_centers.append(self._data[cluster_center_index, :])
            self._clusters.append([])

    def _get_closest_cluster_center(self, sample: np.ndarray) -> int:
        min_index = -1
        min_dist  = 1e32
        for cluster_center_index, cluster_center in enumerate(self._clusters_centers):
            dist = distance(cluster_center, sample)
            if dist > min_dist:
                continue
            min_index = cluster_center_index
            min_dist = dist
        return min_index

    def _clusterize_step(self) -> List[np.ndarray]:
        for cluster in self._clusters:
            cluster.clear()
        # поиск ближайшего центра кластера для конкретной точки
        for sample_index, sample in enumerate(self._data):
            cluster_index = self._get_closest_cluster_center(sample)
            self._clusters[cluster_index].append(sample_index)
        # рассчёт центройдов:
        centroids = []
        for cluster_id, cluster_sample_indices in enumerate(self._clusters):
            if cluster_sample_indices == 0:
                continue
            centroids.append(sum(self._data[sample_index, :] for sample_index in cluster_sample_indices) /
                             len(cluster_sample_indices))

    def _train(self):
        self._create_start_clusters_centers()
        prev_centroids = self._clusters_centers
        while True:
            curr_centroids = self._clusterize_step()
            if all(distance(left, right) < self._distance_threshold for left, right in
                   zip(prev_centroids, curr_centroids)):
                break
            prev_centroids, self._clusters_centers = self._clusters_centers, curr_centroids



