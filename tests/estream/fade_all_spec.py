from expects import equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

from tests.utils import add_vector

with description('E-Stream:') as self:

    """
    Fading operation
    """
    with context('When fading all clusters,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.estream = EStream()
            self.estream._EStream__clusters = [FadingCluster([-1.5, 2.0]),
                                               FadingCluster([2.0, 1.0]),
                                               FadingCluster([3.5, -1.0])]

            self.estream._EStream__fade_all()
        
        with it('should have the updated weights.'):
            weights = [round(cluster.weight, 2) for cluster in self.estream._EStream__clusters]

            expect(weights).to(equal([0.99, 0.99, 0.99]))
        
        with it('should have the updated LS.'):
            LS_1 = [round(ls, 2) for ls in self.estream._EStream__clusters[0].LS]
            LS_2 = [round(ls, 2) for ls in self.estream._EStream__clusters[1].LS]
            LS_3 = [round(ls, 2) for ls in self.estream._EStream__clusters[2].LS]

            expect(LS_1).to(equal([-1.49, 1.99]))
            expect(LS_2).to(equal([1.99, 0.99]))
            expect(LS_3).to(equal([3.48, -0.99]))
        
        with it('should have the updates SS.'):
            SS_1 = [round(ss, 2) for ss in self.estream._EStream__clusters[0].SS]
            SS_2 = [round(ss, 2) for ss in self.estream._EStream__clusters[1].SS]
            SS_3 = [round(ss, 2) for ss in self.estream._EStream__clusters[2].SS]

            expect(SS_1).to(equal([2.23, 3.97]))
            expect(SS_2).to(equal([3.97, 0.99]))
            expect(SS_3).to(equal([12.17, 0.99]))
        
        with it('should have the updates histograms.'):
            for cluster in self.estream._EStream__clusters:
                heights_1 = [round(height, 2) for height in cluster.histograms[0].heights]
                heights_2 = [round(height, 2) for height in cluster.histograms[1].heights]

                expect(heights_1).to(equal([0.99, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]))
                expect(heights_2).to(equal([0.99, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]))
        
        with after.all:
            del self.estream
