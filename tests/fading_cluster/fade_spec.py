from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    """
    Fading operation
    """
    with context('When fading the fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])

            self.fading_cluster.fade(0.99)
        
        with it('should have an updated weight.'):
            expect(self.fading_cluster.weight).to(equal(0.99))
        
        with it('should have the updated LS.'):
            LS = [round(ls, 2) for ls in self.fading_cluster.LS]

            expect(LS).to(equal([-1.48, 1.98]))
        
        with it('should have the updated SS.'):
            SS = [round(ss, 2) for ss in self.fading_cluster.SS]

            expect(SS).to(equal([2.23, 3.96]))
        
        with it('should have the updated histograms.'):
            heights_1 = [round(height, 2) for height in self.fading_cluster.histograms[0].heights]
            heights_2 = [round(height, 2) for height in self.fading_cluster.histograms[1].heights]

            expect(heights_1).to(equal([0.99, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]))
            expect(heights_2).to(equal([0.99, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]))
        
        with after.all:
            del self.fading_cluster
