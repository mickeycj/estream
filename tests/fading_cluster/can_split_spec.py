from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    def add(self, cluster, vector):
        fading_factor = 0.99

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

    with context('When check whether the fading cluster can be splitted'):

        with context('and the split does not appear,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([2.0, 1.0])
                self.add(self.fading_cluster, [2.0, 1.0])
                self.add(self.fading_cluster, [2.0, 1.0])
                self.add(self.fading_cluster, [2.0, 1.0])
                self.add(self.fading_cluster, [2.0, 1.0])

                self.split_index, self.split_attribute = self.fading_cluster.can_split()
            
            with it('should return the split index of -1.'):
                expect(self.split_index).to(equal(-1))
            
            with it('should return the split attribute of -1.'):
                expect(self.split_attribute).to(equal(-1))
            
            with after.all:
                del self.fading_cluster
                del self.split_index
                del self.split_attribute

        with context('and the split appears first,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-5.0, 1.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [-5.0, 1.0])
                for _ in range(9):
                    self.add(self.fading_cluster, [-4.5, 1.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [-3.5, 1.0])
                for _ in range(10):
                    self.add(self.fading_cluster, [-2.5, 1.0])
                for _ in range(12):
                    self.add(self.fading_cluster, [-1.0, 1.0])
                for _ in range(2):
                    self.add(self.fading_cluster, [0.5, 1.0])
                for _ in range(2):
                    self.add(self.fading_cluster, [1.0, 1.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [2.0, 1.0])
                for _ in range(10):
                    self.add(self.fading_cluster, [3.5, 1.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [4.0, 1.0])

                self.split_index, self.split_attribute = self.fading_cluster.can_split()
            
            with it('should return the split index of 5.'):
                expect(self.split_index).to(equal(5))
            
            with it('should return the split attribute of 0.'):
                expect(self.split_attribute).to(equal(0))
            
            with after.all:
                del self.fading_cluster
                del self.split_index
                del self.split_attribute

        with context('and the split appears last,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([1.0, -5.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [1.0, -5.0])
                for _ in range(9):
                    self.add(self.fading_cluster, [1.0, -4.5])
                for _ in range(11):
                    self.add(self.fading_cluster, [1.0, -3.5])
                for _ in range(10):
                    self.add(self.fading_cluster, [1.0, -2.5])
                for _ in range(12):
                    self.add(self.fading_cluster, [1.0, -1.0])
                for _ in range(2):
                    self.add(self.fading_cluster, [1.0, 0.5])
                for _ in range(2):
                    self.add(self.fading_cluster, [1.0, 1.0])
                for _ in range(11):
                    self.add(self.fading_cluster, [1.0, 2.0])
                for _ in range(10):
                    self.add(self.fading_cluster, [1.0, 3.5])
                for _ in range(11):
                    self.add(self.fading_cluster, [1.0, 4.0])

                self.split_index, self.split_attribute = self.fading_cluster.can_split()
            
            with it('should return the split index of 5.'):
                expect(self.split_index).to(equal(5))
            
            with it('should return the split attribute of 1.'):
                expect(self.split_attribute).to(equal(1))
            
            with after.all:
                del self.fading_cluster
                del self.split_index
                del self.split_attribute
