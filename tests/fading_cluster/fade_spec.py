from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    with context('When fading the fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])

            self.fading_cluster.fade(0.9)
        
        with it('should have an updated weight.'):
            expect(self.fading_cluster.weight).to(equal(0.9))
        
        with it('should have the updated LS.'):
            LS = [round(ls, 2) for ls in self.fading_cluster.LS]
            expect(LS).to(equal([-1.35, 1.80]))
        
        with it('should have the updated SS.'):
            SS = [round(ss, 2) for ss in self.fading_cluster.SS]
            expect(SS).to(equal([2.02, 3.60]))
        
        with it('should have the updated histograms.'):
            heights_1 = [round(height, 1) for height in self.fading_cluster.histograms[0].heights]
            heights_2 = [round(height, 1) for height in self.fading_cluster.histograms[1].heights]

            expect(heights_1).to(equal([0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            expect(heights_2).to(equal([0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
        
        with after.all:
            del self.fading_cluster
