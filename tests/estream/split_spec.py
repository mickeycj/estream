from expects import equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

from tests.utils import add_vector

with description('E-Stream:') as self:

    """
    Splitting operation
    """
    with context('When trying to split any cluster'):

        with context('and there is no cluster to split,'):

            with before.all:
                FadingCluster.id_counter = 0

                clusters = []
                for vector in [[-1.5, 2.0], [2.0, 1.0], [3.5, -1.0]]:
                    cluster = FadingCluster(vector)
                    for _ in range(4):
                        add_vector(cluster, vector)
                    cluster.is_active = True
                    
                    clusters.append(cluster)
                
                self.estream = EStream()
                self.estream._EStream__clusters = clusters

                self.estream._EStream__try_split()
            
            with it('should have the same number of clusters.'):
                expect(self.estream.num_clusters).to(equal(3))
            
            with after.all:
                del self.estream

        with context('and there is at least one cluster to split,'):

            with before.all:
                FadingCluster.id_counter = 0

                cluster_1 = FadingCluster([-1.5, 2.0])
                for _ in range(4):
                    add_vector(cluster_1, [-1.5, 2.0])
                cluster_1.is_active = True

                cluster_2 = FadingCluster([-5.0, 1.0])
                for _ in range(11):
                    add_vector(cluster_2, [-5.0, 1.0])
                for _ in range(9):
                    add_vector(cluster_2, [-4.5, 1.0])
                for _ in range(11):
                    add_vector(cluster_2, [-3.5, 1.0])
                for _ in range(10):
                    add_vector(cluster_2, [-2.5, 1.0])
                for _ in range(12):
                    add_vector(cluster_2, [-1.0, 1.0])
                for _ in range(2):
                    add_vector(cluster_2, [0.5, 1.0])
                for _ in range(2):
                    add_vector(cluster_2, [1.0, 1.0])
                for _ in range(11):
                    add_vector(cluster_2, [2.0, 1.0])
                for _ in range(10):
                    add_vector(cluster_2, [3.5, 1.0])
                for _ in range(11):
                    add_vector(cluster_2, [4.0, 1.0])
                cluster_2.is_active = True
                
                cluster_3 = FadingCluster([3.5, -1.0])
                for _ in range(4):
                    add_vector(cluster_3, [3.5, -1.0])
                cluster_3.is_active = True

                self.estream = EStream()
                self.estream._EStream__clusters = [cluster_1, cluster_2, cluster_3]

                self.estream._EStream__try_split()
                self.old_cluster = self.estream._EStream__clusters[1]
                self.new_cluster = self.estream._EStream__clusters[-1]
            
            with it('should add a new cluster.'):
                expect(self.estream.num_clusters).to(equal(4))
            
            with it('should have the updated weight for the old cluster'):
                expect(round(self.old_cluster.weight, 1)).to(equal(30.4))
            
            with it('should have the updated LS for the old cluster.'):
                LS = [round(ls, 1) for ls in self.old_cluster.LS]
                expect(LS).to(equal([-88.5, 30.4]))
            
            with it('should have the updated SS for the old cluster.'):
                SS = [round(ss, 1) for ss in self.old_cluster.SS]
                expect(SS).to(equal([323.7, 30.4]))
            
            with it('should have the updated histogram at the split attribute for the old cluster.'):
                heights = [round(height, 1) for height in self.old_cluster.histograms[0].heights]
                expect(heights).to(equal([5.6, 4.9, 3.4, 3.1, 2.9, 2.6, 2.6, 2.7, 1.6, 1.0]))
            
            with it('should have the updated histogram at the other attribute for the old cluster.'):
                heights = [round(height, 1) for height in self.old_cluster.histograms[1].heights]
                expect(heights).to(equal([30.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
            with it('should have the weight for the new cluster'):
                expect(round(self.new_cluster.weight, 1)).to(equal(29.1))
            
            with it('should have the LS for the new cluster.'):
                LS = [round(ls, 1) for ls in self.new_cluster.LS]
                expect(LS).to(equal([78.7, 29.1]))
            
            with it('should have the SS for the new cluster.'):
                SS = [round(ss, 1) for ss in self.new_cluster.SS]
                expect(SS).to(equal([242.3, 29.1]))
            
            with it('should have the histogram at the split attribute for the new cluster.'):
                heights = [round(height, 1) for height in self.new_cluster.histograms[0].heights]
                expect(heights).to(equal([1.5, 1.5, 1.8, 2.0, 2.0, 2.3, 2.3, 4.1, 5.8, 5.8]))
            
            with it('should have the histogram at the other attribute for the new cluster.'):
                heights = [round(height, 1) for height in self.new_cluster.histograms[1].heights]
                expect(heights).to(equal([29.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
            with after.all:
                del self.estream
                del self.old_cluster
                del self.new_cluster
