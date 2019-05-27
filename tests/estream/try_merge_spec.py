from expects import equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

from tests.utils import add_vector

with description('E-Stream:') as self:

    """
    Merging operation
    """
    with context('When trying to merge any pair of clusters'):

        with context('and there is not a pair of clusters close together,'):

            with before.all:
                FadingCluster.id_counter = 0

                cluster_1 = FadingCluster([-1.5, 2.0])
                add_vector(cluster_1, [-1.0, 2.0])
                add_vector(cluster_1, [-1.5, 1.5])
                add_vector(cluster_1, [-2.0, 1.0])
                add_vector(cluster_1, [-2.0, 2.0])
                cluster_1.is_active = True

                cluster_2 = FadingCluster([1.5, -2.0])
                add_vector(cluster_2, [1.0, -2.0])
                add_vector(cluster_2, [1.5, -1.5])
                add_vector(cluster_2, [2.0, -1.0])
                add_vector(cluster_2, [2.0, -2.0])
                cluster_2.is_active = True

                self.estream = EStream()
                self.estream._EStream__clusters = [cluster_1, cluster_2]

                self.estream._EStream__try_merge()
            
            with it('should have the same number of clusters.'):
                expect(self.estream.num_clusters).to(equal(2))
            
            with after.all:
                del self.estream

        with context('and there is a pair of clusters close together,'):

            with before.all:
                FadingCluster.id_counter = 0

                cluster_1 = FadingCluster([1.5, 2.0])
                add_vector(cluster_1, [-1.0, 2.0])
                add_vector(cluster_1, [-1.5, 1.5])
                add_vector(cluster_1, [-2.0, 1.0])
                add_vector(cluster_1, [2.0, 2.0])
                cluster_1.is_active = True

                cluster_2 = FadingCluster([0.5, 2.0])
                add_vector(cluster_2, [-1.0, 1.0])
                add_vector(cluster_2, [0.5, 1.5])
                add_vector(cluster_2, [0.0, 2.0])
                add_vector(cluster_2, [2.0, 2.0])
                cluster_2.is_active = True

                self.estream = EStream()
                self.estream._EStream__clusters = [cluster_1, cluster_2]

                self.estream._EStream__try_merge()
                self.merged_cluster = self.estream._EStream__clusters[0]
            
            with it('should have one fewer clusters.'):
                expect(self.estream.num_clusters).to(equal(1))
        
            with it('should have the updated weight for the merged cluster.'):
                expect(round(self.merged_cluster.weight, 1)).to(equal(9.8))
            
            with it('should have the updated LS for the merged cluster.'):
                LS = [round(ls, 1) for ls in self.merged_cluster.LS]

                expect(LS).to(equal([1.0, 16.7]))
            
            with it('should have the updated SS for the merged cluster.'):
                SS = [round(ss, 1) for ss in self.merged_cluster.SS]
                
                expect(SS).to(equal([18.8, 29.9]))
            
            with it('should have the updated heights for the histograms for the merged cluster.'):
                heights_1 = [round(height, 1) for height in self.merged_cluster.histograms[0].heights]
                heights_2 = [round(height, 1) for height in self.merged_cluster.histograms[1].heights]

                expect(heights_1).to(equal([1.1, 0.7, 1.4, 0.7, 0.3, 2.0, 0.6, 0.1, 0.8, 2.0]))
                expect(heights_2).to(equal([2.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 5.9]))
            
            with after.all:
                del self.estream
                del self.merged_cluster
