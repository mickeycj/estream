from expects import be_false, be_true, equal, expect
from mamba import after, before, context, description, it

from estream import Histogram

with description('Histogram:') as self:
    
    """
    Adding operation
    """
    with context('When adding the first value,'):

        with before.all:
            self.histogram = Histogram()
            self.histogram.add(1.0)
        
        with it('should now have a minimum value.'):
            expect(self.histogram.has_min).to(be_true)
        
        with it('should have the speicified value as the minimum value.'):
            expect(self.histogram.min).to(equal(1.0))

        with it('should have the speicified height as the first height.'):
            expect(self.histogram.heights[0]).to(equal(1.0))
        
        with after.all:
            del self.histogram
    
    with context('When adding the second value'):
        
        with context('and the value is less than the minimum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(1.0, 2.0)
                self.histogram.add(0.0)
            
            with it('should now have a maximum value.'):
                expect(self.histogram.has_max).to(be_true)
            
            with it('should have the old minimum value as the maximum value.'):
                expect(self.histogram.max).to(equal(1.0))
            
            with it('should have the specified value as the minimum value.'):
                expect(self.histogram.min).to(equal(0.0))
            
            with it('should have the old first height as the last height.'):
                expect(self.histogram.heights[-1]).to(equal(2.0))
            
            with it('should have the specified height as the first height.'):
                expect(self.histogram.heights[0]).to(equal(1.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram.width).to(equal(0.1))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]))
        
            with after.all:
                del self.histogram
        
        with context('and the value is more than the minimum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(1.0, 2.0)
                self.histogram.add(2.0)
            
            with it('should now have a maximum value.'):
                expect(self.histogram.has_max).to(be_true)
            
            with it('should have the specified value as the maximum value.'):
                expect(self.histogram.max).to(equal(2.0))
            
            with it('should have the specified height as the last height.'):
                expect(self.histogram.heights[-1]).to(equal(1.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram.width).to(equal(0.1))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]))
            
            with after.all:
                del self.histogram
        
        with context('and the value is equal to the minimum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(1.0, 2.0)
                self.histogram.add(1.0)
            
            with it('should still not have a maximum value.'):
                expect(self.histogram.has_max).to(be_false)
            
            with it('should add the specified height to the first height.'):
                expect(self.histogram.heights[0]).to(equal(3.0))
            
            with after.all:
                del self.histogram
        
    with context('When adding any following arbitrary value'):

        with context('and the value is less than the minimum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(2.0, 5.0)
                self.histogram.add(5.0, 2.0)
                self.histogram.add(1.0)
            
            with it('should have the specified value as the minimum value.'):
                expect(self.histogram.min).to(equal(1.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram.width).to(equal(0.4))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram.heights]
                expect(heights).to(equal([1.0, 0.0, 3.3, 1.7, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram

        with context('and the value is more than the maximum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(2.0, 5.0)
                self.histogram.add(5.0, 2.0)
                self.histogram.add(6.0)
            
            with it('should have the specified value as the maximum value.'):
                expect(self.histogram.max).to(equal(6.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram.width).to(equal(0.4))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 1.3, 0.0, 1.0]))
            
            with after.all:
                del self.histogram
        
        with context('and the value is between the minimum and maximum value,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(2.0, 5.0)
                self.histogram.add(5.0, 2.0)
                self.histogram.add(3.5, 3.5)
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 3.5, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram
