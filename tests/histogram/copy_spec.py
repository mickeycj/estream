from copy import copy, deepcopy
from sys import maxsize

from expects import be_false, equal, expect
from mamba import after, before, context, description, it

from estream import Histogram

with description('Histogram:') as self:
    
    """
    Copying operations
    """
    with context('When making a shallow copy,'):

        with before.all:
            self.histogram = Histogram()
            self.copy = copy(self.histogram)
        
        with it('should return an exact copy.'):
            expect(self.copy.has_min).to(be_false)
            expect(self.copy.has_max).to(be_false)
            expect(self.copy.min).to(equal(-maxsize))
            expect(self.copy.max).to(equal(maxsize))
            expect(self.copy.size).to(equal(10))
            expect(self.copy.width).to(equal(0.0))
            expect(self.copy.heights).to(equal([0.0] * 10))
            expect(self.copy.upper_bounds).to(equal([0.0] * 10))
            expect(self.copy._Histogram__significant).to(equal(3.843))
            expect(self.copy._Histogram__sensitivity).to(equal(5))
        
        with it('should share the same instances of attributes.'):
            self.histogram.heights[0] = 1.0
            self.histogram.upper_bounds[0] = 2.0

            expect(self.copy.heights[0]).to(equal(1.0))
            expect(self.copy.upper_bounds[0]).to(equal(2.0))
        
        with after.all:
            del self.histogram
            del self.copy
    
    with context('When making a deep copy,'):

        with before.all:
            self.histogram = Histogram()
            self.copy = deepcopy(self.histogram)
        
        with it('should return an exact copy.'):
            expect(self.copy.has_min).to(be_false)
            expect(self.copy.has_max).to(be_false)
            expect(self.copy.min).to(equal(-maxsize))
            expect(self.copy.max).to(equal(maxsize))
            expect(self.copy.size).to(equal(10))
            expect(self.copy.width).to(equal(0.0))
            expect(self.copy.heights).to(equal([0.0] * 10))
            expect(self.copy.upper_bounds).to(equal([0.0] * 10))
            expect(self.copy._Histogram__significant).to(equal(3.843))
            expect(self.copy._Histogram__sensitivity).to(equal(5))
        
        with it('should not share the same instances of attributes.'):
            self.histogram.heights[0] = 1.0
            self.histogram.upper_bounds[0] = 2.0

            expect(self.copy.heights[0]).not_to(equal(1.0))
            expect(self.copy.upper_bounds[0]).not_to(equal(2.0))

        with after.all:
            del self.histogram
            del self.copy
