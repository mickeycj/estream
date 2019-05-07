from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    def add(self, cluster, vector):
        fading_factor = 0.9

        cluster.weight *= fading_factor
        cluster.LS = [ls * fading_factor for ls in cluster.LS]
        cluster.SS = [ss * fading_factor for ss in cluster.SS]
        for histogram in cluster.histograms:
            histogram.heights = [height * fading_factor for height in histogram.heights]

        cluster.weight += 1.0
        cluster.LS = [ls + value for ls, value in zip(cluster.LS, vector)]
        cluster.SS = [ss + value ** 2 for ss, value in zip(cluster.SS, vector)]
        for histogram, value in zip(cluster.histograms, vector):
            histogram.add(value)

    with context('When computing distance to another fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster_1 = FadingCluster([-1.5, 2.0])
            self.add(self.fading_cluster_1, [-1.0, 2.0])
            self.add(self.fading_cluster_1, [-1.5, 1.5])
            self.add(self.fading_cluster_1, [-2.0, 1.0])
            self.add(self.fading_cluster_1, [-2.0, 2.0])

            self.fading_cluster_2 = FadingCluster([1.5, -2.0])
            self.add(self.fading_cluster_2, [1.0, -2.0])
            self.add(self.fading_cluster_2, [1.5, -1.5])
            self.add(self.fading_cluster_2, [2.0, -1.0])
            self.add(self.fading_cluster_2, [2.0, -2.0])

            self.distance = self.fading_cluster_1.get_center_distance(self.fading_cluster_2)
        
        with it('should return the estimated distance between the two fading clusters.'):
            expect(round(self.distance, 1)).to(equal(3.3))
        
        with after.all:
            del self.fading_cluster_1
            del self.fading_cluster_2
            del self.distance

    with context('When computing distance to another vector,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])
            self.add(self.fading_cluster, [-1.0, 2.0])
            self.add(self.fading_cluster, [-1.5, 1.5])
            self.add(self.fading_cluster, [-2.0, 1.0])
            self.add(self.fading_cluster, [-2.0, 2.0])

            self.distance = self.fading_cluster.get_normalized_distance([1.6, -1.7])
        
        with it('should return the estimated distance between the fading cluster and the vector.'):
            expect(round(self.distance, 1)).to(equal(8.5))
        
        with after.all:
            del self.fading_cluster
            del self.distance
