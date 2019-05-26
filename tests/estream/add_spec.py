from expects import equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

from tests.utils import add_vector

with description('E-Stream:') as self:

    """
    Adding operation
    """
    with context('When adding the first vector,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.estream = EStream()

            self.estream._EStream__add([-1.5, 2.0])
            self.cluster = self.estream._EStream__clusters[0]
        
        with it('should have one cluster.'):
            expect(len(self.estream._EStream__clusters)).to(equal(1))
        
        with it('should have a cluster with initial weight.'):
            expect(round(self.cluster.weight, 1)).to(equal(1.0))
        
        with it('should have the LS from the specified vector.'):
            LS = [round(ls, 1) for ls in self.cluster.LS]
            expect(LS).to(equal([-1.5, 2.0]))
        
        with it('should have the SS from the specified vector.'):
            SS = [round(ss, 1) for ss in self.cluster.SS]
            expect(SS).to(equal([2.2, 4.0]))
        
        with it('should have the histograms from the specified vector.'):
            heights_1 = [round(height, 1) for height in self.cluster.histograms[0].heights]
            heights_2 = [round(height, 1) for height in self.cluster.histograms[1].heights]

            expect(heights_1).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            expect(heights_2).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
        
        with after.all:
            del self.estream
            del self.cluster
    
    with context('When adding another vector'):

        with context('and it is not close to an existing cluster,'):

            with before.all:
                FadingCluster.id_counter = 0

                cluster_1 = FadingCluster([-3.0, 4.0])
                add_vector(cluster_1, [-2.0, 4.0])
                add_vector(cluster_1, [-3.0, 3.0])
                add_vector(cluster_1, [-4.0, 2.0])
                add_vector(cluster_1, [-4.0, 4.0])

                cluster_2 = FadingCluster([1.5, 2.0])
                add_vector(cluster_2, [-1.0, 2.0])
                add_vector(cluster_2, [-1.5, 1.5])
                add_vector(cluster_2, [-2.0, 1.0])
                add_vector(cluster_2, [2.0, 2.0])
                cluster_2.is_active = True

                self.estream = EStream()
                self.estream._EStream__clusters = [cluster_1, cluster_2]

                self.estream._EStream__add([-3.5, 5.0])
                self.new_cluster = self.estream._EStream__clusters[-1]
            
            with it('should have one more clusters.'):
                expect(len(self.estream.clusters)).to(equal(3))
            
            with it('should have a weight for the new cluster.'):
                expect(round(self.new_cluster.weight, 1)).to(equal(1.0))
            
            with it('should have the LS for the new cluster.'):
                LS = [round(ls, 1) for ls in self.new_cluster.LS]
                expect(LS).to(equal([-3.5, 5.0]))

            with it('should have the SS for the new cluster.'):
                SS = [round(ss, 1) for ss in self.new_cluster.SS]
                expect(SS).to(equal([12.2, 25.0]))
            
            with it('should have the histograms for the new cluster.'):
                heights_1 = [round(height, 1) for height in self.new_cluster.histograms[0].heights]
                heights_2 = [round(height, 1) for height in self.new_cluster.histograms[1].heights]

                expect(heights_1).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
                expect(heights_2).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
            with after.all:
                del self.estream
                del self.new_cluster

        with context('and it is close to an existing cluster,'):

            with before.all:
                FadingCluster.id_counter = 0

                cluster_1 = FadingCluster([-3.0, 4.0])
                add_vector(cluster_1, [-2.0, 4.0])
                add_vector(cluster_1, [-3.0, 3.0])
                add_vector(cluster_1, [-4.0, 2.0])
                add_vector(cluster_1, [-4.0, 4.0])

                cluster_2 = FadingCluster([1.5, 2.0])
                add_vector(cluster_2, [-1.0, 2.0])
                add_vector(cluster_2, [-1.5, 1.5])
                add_vector(cluster_2, [-2.0, 1.0])
                add_vector(cluster_2, [2.0, 2.0])
                cluster_2.is_active = True

                self.estream = EStream()
                self.estream._EStream__clusters = [cluster_1, cluster_2]

                self.estream._EStream__add([0.0, 1.5])
                self.merged_cluster = self.estream._EStream__clusters[1]
            
            with it('should have the same number of clusters.'):
                expect(len(self.estream.clusters)).to(equal(2))
            
            with it('should have an updated weight for the merged cluster.'):
                expect(round(self.merged_cluster.weight, 1)).to(equal(5.9))
            
            with it('should have the updated LS for the merged cluster.'):
                LS = [round(ls, 1) for ls in self.merged_cluster.LS]
                expect(LS).to(equal([-1.0, 9.8]))

            with it('should have the updated SS for the merged cluster.'):
                SS = [round(ss, 1) for ss in self.merged_cluster.SS]
                expect(SS).to(equal([13.3, 17.2]))
            
            with it('should have the updated histograms for the merged cluster.'):
                heights_1 = [round(height, 1) for height in self.merged_cluster.histograms[0].heights]
                heights_2 = [round(height, 1) for height in self.merged_cluster.histograms[1].heights]

                expect(heights_1).to(equal([1.1, 0.7, 0.7, 0.4, 1.0, 0.0, 0.0, 0.1, 0.8, 1.0]))
                expect(heights_2).to(equal([1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 2.9]))
            
            with after.all:
                del self.estream
                del self.merged_cluster
