from expects import be_false, be_true, equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

with description('E-Stream:') as self:

    """
    Initializing operation
    """
    with context('When fitting the first vector, '):

        with before.all:
            FadingCluster.id_counter = 0

            self.estream = EStream()

            self.estream._EStream__initialize([1.5, 2.0])
        
        with it('should set its state to initialized.'):
            expect(self.estream._EStream__is_initialized).to(be_true)
        
        with it('should now contain one inactive cluster.'):
            expect(len(self.estream.clusters)).to(equal(1))
            expect(len(self.estream.active_clusters)).to(equal(0))
            expect(len(self.estream.inactive_clusters)).to(equal(1))
            expect(self.estream.clusters[0].is_active).to(be_false)
        
        with after.all:
            del self.estream
