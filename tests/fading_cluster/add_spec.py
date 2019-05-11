from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    with context('When adding new data to the fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([1.5, 2.0])

            self.fading_cluster.add([4.5, -1.5])
        
        with it('should have the updated weight.'):
            expect(round(self.fading_cluster.weight, 1)).to(equal(2.0))
        
        with it('should have the updated LS.'):
            LS = [round(ls, 1) for ls in self.fading_cluster.LS]
            expect(LS).to(equal([6.0, 0.5]))
        
        with it('should have the updated SS.'):
            SS = [round(ss, 1) for ss in self.fading_cluster.SS]
            expect(SS).to(equal([22.5, 6.2]))
        
        with it('should have the updated heights for the histograms.'):
            heights_1 = [round(height, 1) for height in self.fading_cluster.histograms[0].heights]
            heights_2 = [round(height, 1) for height in self.fading_cluster.histograms[1].heights]

            expect(heights_1).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]))
            expect(heights_2).to(equal([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]))
        
        with after.all:
            del self.fading_cluster
