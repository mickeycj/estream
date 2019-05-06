from expects import be_none, equal, expect
from mamba import after, before, context, description, it

from estream import Histogram

with description('Histogram:') as self:

    """
    Splitting operation
    """
    with context('When splitting two histograms'):

        with context('and the specified index is -1,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(1.0)
                self.histogram.add(2.0)
                self.histogram.add(3.0)

                self.new_histogram = self.histogram.split(-1)
            
            with it('should not return a histogram.'):
                expect(self.new_histogram).to(be_none)
            
            with after.all:
                del self.histogram
                del self.new_histogram
        
        with context('and the histogram\'s weight is left-heavy,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(-5.0, 12.0)
                self.histogram.add(-4.5, 9.0)
                self.histogram.add(-3.5, 10.5)
                self.histogram.add(-2.5, 9.5)
                self.histogram.add(-1.0, 11.5)
                self.histogram.add(0.5, 2.0)
                self.histogram.add(1.0, 1.5)
                self.histogram.add(2.0, 11.0)
                self.histogram.add(3.5, 10.5)
                self.histogram.add(4.0, 11.0)

                self.new_histogram = self.histogram.split(5)
            
            with it('should have the specified upper bound as the new maximum value for the original histogram.'):
                expect(round(self.histogram.max, 1)).to(equal(0.4))
            
            with it('should have an updated with for each bar for the original histogram.'):
                expect(round(self.histogram.width, 2)).to(equal(0.54))
            
            with it('should have an updated upper bound for each bar for the original histogram.'):
                upper_bounds = [round(upper_bound, 2) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([-4.46, -3.92, -3.38, -2.84, -2.30, -1.76, -1.22, -0.68, -0.14, 0.40]))
            
            with it('should have the updated heights for the original histogram.'):
                heights = [round(height, 1) for height in self.histogram.heights]
                expect(heights).to(equal([12.1, 10.2, 6.2, 5.3, 4.8, 4.0, 3.9, 3.9, 2.2, 1.4]))
            
            with it('should have the specified upper bound as the minimum value for the new histogram.'):
                expect(round(self.new_histogram.min, 1)).to(equal(0.4))
            
            with it('should have the original\'s maximum value as the maximum value for the new histogram.'):
                expect(round(self.new_histogram.max, 1)).to(equal(4.0))
            
            with it('should have the width for each bar for the new histogram.'):
                expect(round(self.new_histogram.width, 2)).to(equal(0.36))
            
            with it('should have the upper bound for each bar for the new histogram.'):
                upper_bounds = [round(upper_bound, 2) for upper_bound in self.new_histogram.upper_bounds]
                expect(upper_bounds).to(equal([0.76, 1.12, 1.48, 1.84, 2.20, 2.56, 2.92, 3.28, 3.64, 4.00]))
            
            with it('should have the heights for the new histogram.'):
                heights = [round(height, 1) for height in self.new_histogram.heights]
                expect(heights).to(equal([1.9, 1.9, 2.3, 2.6, 2.6, 2.9, 2.9, 4.6, 6.4, 6.4]))
            
            with after.all:
                del self.histogram
                del self.new_histogram
        
        with context('and the histogram\'s weight is right-heavy,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(-5.0, 11.0)
                self.histogram.add(-4.5, 10.5)
                self.histogram.add(-3.5, 11.0)
                self.histogram.add(-2.5, 1.5)
                self.histogram.add(-1.0, 2.0)
                self.histogram.add(0.5, 11.5)
                self.histogram.add(1.0, 9.5)
                self.histogram.add(2.0, 10.5)
                self.histogram.add(3.5, 9.0)
                self.histogram.add(4.0, 12.0)

                self.new_histogram = self.histogram.split(3)
            
            with it('should have the specified upper bound as the new minimum value for the original histogram.'):
                expect(round(self.histogram.min, 1)).to(equal(-1.4))
            
            with it('should have an updated with for each bar for the original histogram.'):
                expect(round(self.histogram.width, 2)).to(equal(0.54))
            
            with it('should have an updated upper bound for each bar for the original histogram.'):
                upper_bounds = [round(upper_bound, 2) for upper_bound in self.histogram.upper_bounds]
                expect(upper_bounds).to(equal([-0.86, -0.32, 0.22, 0.76, 1.30, 1.84, 2.38, 2.92, 3.46, 4.00]))
            
            with it('should have the updated heights for the original histogram.'):
                heights = [round(height, 1) for height in self.histogram.heights]
                expect(heights).to(equal([1.5, 2.6, 4.7, 6.6, 7.6, 4.9, 4.5, 3.8, 7.8, 9.7]))
            
            with it('should have the original\'s maximum value as the minimum value for the new histogram.'):
                expect(round(self.new_histogram.min, 1)).to(equal(-5.0))
            
            with it('should have the specified upper bound as the maximum value for the new histogram.'):
                expect(round(self.new_histogram.max, 1)).to(equal(-1.4))
            
            with it('should have the width for each bar for the new histogram.'):
                expect(round(self.new_histogram.width, 2)).to(equal(0.36))
            
            with it('should have the upper bound for each bar for the new histogram.'):
                upper_bounds = [round(upper_bound, 2) for upper_bound in self.new_histogram.upper_bounds]
                expect(upper_bounds).to(equal([-4.64, -4.28, -3.92, -3.56, -3.20, -2.84, -2.48, -2.12, -1.76, -1.40]))
            
            with it('should have the heights for the new histogram.'):
                heights = [round(height, 1) for height in self.new_histogram.heights]
                expect(heights).to(equal([8.1, 8.1, 6.0, 3.8, 3.8, 1.5, 1.5, 1.0, 0.5, 0.5]))
            
            with after.all:
                del self.histogram
                del self.new_histogram
