from clusterization.methods.clusterizer import Clusterizer
from model.point import Point


class UnionAlgo(Clusterizer):
    def __init__(self, dataset: list[Point], count_cluster: int=2) -> None:
        super().__init__(dataset, count_cluster)
    
    def evalute(self) -> None:
        steps = []
        clusters = []
        for point in self.dataset:
            clusters.append([point])
        steps.append([[point.id_point] for point in self.dataset])

        for _ in range(self.size - self.count_cluster):
            nearest_cluster = None
            min_dist = None
            for i, first_cluster in enumerate(clusters):
                first_center = Point.mid_point(*first_cluster)
                for second_cluster in clusters[i+1:]:
                    second_centr = Point.mid_point(*second_cluster)
                    dist = Point.distance_between_points(first_center, second_centr)
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        nearest_cluster = (first_cluster, second_cluster)
            
            clusters = [cluster for cluster in clusters if cluster not in nearest_cluster]
            clusters.append(nearest_cluster[0] + nearest_cluster[1])

            all_ids = []
            for cluster in clusters:
                all_ids.append([point.id_point for point in cluster])
            steps.append(all_ids)

        labels = []
        for i, cluster in enumerate(clusters):
            for point in cluster:
                labels.append(str(i+1))

        self._data['labels'] = labels

        for step in steps:
            print(step)
