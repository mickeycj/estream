from copy import copy, deepcopy

from expects import be_false, be_true, equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    """
    Copying operations
    """
    with context('When making a shallow copy,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])

            self.copy = copy(self.fading_cluster)
        
        with it('should return an exact copy.'):
            expect(self.copy.id).to(equal(0))
            expect(self.copy.is_active).to(be_false)
            expect(self.copy.weight).to(equal(1.0))
            expect(self.copy.dimensions).to(equal(2))
            expect(self.copy.LS).to(equal([-1.5, 2.0]))
            expect(self.copy.SS).to(equal([2.25, 4.00]))
            expect(self.copy.histograms[0].has_min).to(be_true)
            expect(self.copy.histograms[0].min).to(equal(-1.5))
            expect(self.copy.histograms[0].heights[0]).to(equal(1.0))
            expect(self.copy.histograms[1].has_min).to(be_true)
            expect(self.copy.histograms[1].min).to(equal(2.0))
            expect(self.copy.histograms[1].heights[0]).to(equal(1.0))
        
        with it('should share the same instances of attributes.'):
            self.fading_cluster.LS[0] = -1.0
            self.fading_cluster.SS[0] = 1.0
            self.fading_cluster.histograms[0].min = -1.0

            expect(self.copy.LS[0]).to(equal(-1.0))
            expect(self.copy.SS[0]).to(equal(1.0))
            expect(self.copy.histograms[0].min).to(equal(-1.0))
        
        with after.all:
            del self.fading_cluster
            del self.copy

    with context('When making a deep copy,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])

            self.copy = deepcopy(self.fading_cluster)
        
        with it('should return an exact copy.'):
            expect(self.copy.id).to(equal(0))
            expect(self.copy.is_active).to(be_false)
            expect(self.copy.weight).to(equal(1.0))
            expect(self.copy.dimensions).to(equal(2))
            expect(self.copy.LS).to(equal([-1.5, 2.0]))
            expect(self.copy.SS).to(equal([2.25, 4.00]))
            expect(self.copy.histograms[0].has_min).to(be_true)
            expect(self.copy.histograms[0].min).to(equal(-1.5))
            expect(self.copy.histograms[0].heights[0]).to(equal(1.0))
            expect(self.copy.histograms[1].has_min).to(be_true)
            expect(self.copy.histograms[1].min).to(equal(2.0))
            expect(self.copy.histograms[1].heights[0]).to(equal(1.0))
        
        with it('should not share the same instances of attributes.'):
            self.fading_cluster.LS[0] = -1.0
            self.fading_cluster.SS[0] = 1.0
            self.fading_cluster.histograms[0].min = -1.0

            expect(self.copy.LS[0]).not_to(equal(-1.0))
            expect(self.copy.SS[0]).not_to(equal(1.0))
            expect(self.copy.histograms[0].min).not_to(equal(-1.0))
        
        with after.all:
            del self.fading_cluster
            del self.copy
    
    with context('When creating a new fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])

            self.copy = FadingCluster.from_fading_cluster(self.fading_cluster)
        
        with it('should return an exact copy with an incremented ID.'):
            expect(self.copy.id).to(equal(1))
            expect(self.copy.is_active).to(be_false)
            expect(self.copy.weight).to(equal(1.0))
            expect(self.copy.dimensions).to(equal(2))
            expect(self.copy.LS).to(equal([-1.5, 2.0]))
            expect(self.copy.SS).to(equal([2.25, 4.00]))
            expect(self.copy.histograms[0].has_min).to(be_true)
            expect(self.copy.histograms[0].min).to(equal(-1.5))
            expect(self.copy.histograms[0].heights[0]).to(equal(1.0))
            expect(self.copy.histograms[1].has_min).to(be_true)
            expect(self.copy.histograms[1].min).to(equal(2.0))
            expect(self.copy.histograms[1].heights[0]).to(equal(1.0))
        
        with it('should not share the same instances of attributes.'):
            self.fading_cluster.LS[0] = -1.0
            self.fading_cluster.SS[0] = 1.0
            self.fading_cluster.histograms[0].min = -1.0

            expect(self.copy.LS[0]).not_to(equal(-1.0))
            expect(self.copy.SS[0]).not_to(equal(1.0))
            expect(self.copy.histograms[0].min).not_to(equal(-1.0))
        
        with after.all:
            del self.fading_cluster
            del self.copy 
