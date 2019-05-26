from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

from tests.utils import add_vector

with description('Fading Cluster:') as self:

    """
    Merging operation
    """
    with context('When merging two fading clusters together,'):

        with before.all:
            FadingCluster.id_counter  = 0

            self.fading_cluster_1 = FadingCluster([1.5, 2.0])
            add_vector(self.fading_cluster_1, [-1.0, 2.0])
            add_vector(self.fading_cluster_1, [-1.5, 1.5])
            add_vector(self.fading_cluster_1, [-2.0, 1.0])
            add_vector(self.fading_cluster_1, [2.0, 2.0])

            self.fading_cluster_2 = FadingCluster([0.5, 2.0])
            add_vector(self.fading_cluster_2, [-1.0, 1.0])
            add_vector(self.fading_cluster_2, [0.5, 1.5])
            add_vector(self.fading_cluster_2, [0.0, 2.0])
            add_vector(self.fading_cluster_2, [2.0, 2.0])

            self.fading_cluster_1.merge(self.fading_cluster_2)
        
        with it('should have the updated weight.'):
            expect(round(self.fading_cluster_1.weight, 1)).to(equal(9.8))
        
        with it('should have the updated LS.'):
            LS = [round(ls, 1) for ls in self.fading_cluster_1.LS]

            expect(LS).to(equal([1.0, 16.7]))
        
        with it('should have the updated SS.'):
            SS = [round(ss, 1) for ss in self.fading_cluster_1.SS]
            
            expect(SS).to(equal([18.8, 29.9]))
        
        with it('should have the updated heights for the histograms.'):
            heights_1 = [round(height, 1) for height in self.fading_cluster_1.histograms[0].heights]
            heights_2 = [round(height, 1) for height in self.fading_cluster_1.histograms[1].heights]

            expect(heights_1).to(equal([1.1, 0.7, 1.4, 0.7, 0.3, 2.0, 0.6, 0.1, 0.8, 2.0]))
            expect(heights_2).to(equal([2.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 5.9]))
        
        with after.all:
            del self.fading_cluster_1
            del self.fading_cluster_2
