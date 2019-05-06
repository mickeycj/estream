from expects import be_false, be_true, equal, expect, raise_error
from mamba import after, before, context, description, it

from estream import Histogram

with description('Histogram:') as self:

    """
    Merging operation
    """
    with context('When merging empty histogram(s)'):

        with context('and the former is empty,'):
            
            with before.all:
                self.histogram_1 = Histogram()

                self.histogram_2 = Histogram()
                self.histogram_2.add(1.0)
            
            with it('should raise an error.'):
                merge = lambda: self.histogram_1.merge(self.histogram_2)
                expect(merge).to(raise_error(ValueError, 'Cannot merge empty histogram(s)!'))

            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the latter is empty,'):
            
            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(1.0)

                self.histogram_2 = Histogram()
            
            with it('should raise an error.'):
                merge = lambda: self.histogram_1.merge(self.histogram_2)
                expect(merge).to(raise_error(ValueError, 'Cannot merge empty histogram(s)!'))

            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and both are empty,'):
            
            with before.all:
                self.histogram_1 = Histogram()

                self.histogram_2 = Histogram()
            
            with it('should raise an error.'):
                merge = lambda: self.histogram_1.merge(self.histogram_2)
                expect(merge).to(raise_error(ValueError, 'Cannot merge empty histogram(s)!'))

            with after.all:
                del self.histogram_1
                del self.histogram_2

    with context('When merging two incomplete histograms'):
        
        with context('and the latter\'s minumum value is less than the former\'s,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(1.0, 2.0)
                
                self.histogram_2 = Histogram()
                self.histogram_2.add(0.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should now have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_true)
            
            with it('should have the former\'s minimum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(1.0))
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(0.0))
            
            with it('should have the former\'s first height as the last height.'):
                expect(self.histogram_1.heights[-1]).to(equal(2.0))
            
            with it('should have the latter\'s first height as the first height.'):
                expect(self.histogram_1.heights[0]).to(equal(1.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.1))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
        
        with context('and the latter\'s minumum value is more than the former\'s,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(1.0, 2.0)
                
                self.histogram_2 = Histogram()
                self.histogram_2.add(2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should now have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_true)
            
            with it('should have the latter\'s minimum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(2.0))
            
            with it('should have the latter\'s first height as the last height.'):
                expect(self.histogram_1.heights[-1]).to(equal(1.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.1))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
        
        with context('and the latter\'s minimum value is equal to the former\'s,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(1.0)
                
                self.histogram_2 = Histogram()
                self.histogram_2.add(1.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should still not have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_false)
            
            with it('should add the latter\'s first height to the former\'s.'):
                expect(self.histogram_1.heights[0]).to(equal(2.0))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
    
    with context('When merging an incomplete histogram with a complete one'):

        with context('and the former\'s minimum value is less than the latter\'s minimum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(1.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(2.0, 5.0)
                self.histogram_2.add(5.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should now have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_true)
            
            with it('should have the latter\'s maximum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(5.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.4))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([1.0, 0.0, 3.3, 1.7, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s minimum value is more than the latter\'s maximum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(6.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(2.0, 5.0)
                self.histogram_2.add(5.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should now have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_true)
            
            with it('should have the former\'s minimum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(6.0))
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(2.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.4))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 1.3, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s minimum value is equal the latter\'s maximum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(3.5, 3.5)

                self.histogram_2 = Histogram()
                self.histogram_2.add(2.0, 5.0)
                self.histogram_2.add(5.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should now have a maximum value.'):
                expect(self.histogram_1.has_max).to(be_true)
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(2.0))
            
            with it('should have the latter\'s maximum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(5.0))
            
            with it('should now have a width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.3))
            
            with it('should now have an upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([2.3, 2.6, 2.9, 3.2, 3.5, 3.8, 4.1, 4.4, 4.7, 5.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 3.5, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
    
    with context('When merging a complete histogram with an incomplete one'):

        with context('and the latter\'s minimum value is less than the former\'s minimum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(2.0, 5.0)
                self.histogram_1.add(5.0, 2.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(1.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(1.0))
            
            with it('should now have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.4))
            
            with it('should now have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.6, 5.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([1.0, 0.0, 3.3, 1.7, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s minimum value is more than the latter\'s maximum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(2.0, 5.0)
                self.histogram_1.add(5.0, 2.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(6.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s maximum value as the maxnimum value.'):
                expect(self.histogram_1.max).to(equal(6.0))
            
            with it('should now have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.4))
            
            with it('should now have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 1.3, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s minimum value is between the latter\'s minimum and maximum value,'):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(2.0, 5.0)
                self.histogram_1.add(5.0, 2.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(3.5, 3.5)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([5.0, 0.0, 0.0, 0.0, 3.5, 0.0, 0.0, 0.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
    
    with context('When merging two histograms'):

        with context('and the former\'s range is absolutely below the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(-3.0, 2.0)
                self.histogram_1.add(-1.0)
                self.histogram_1.add(-5.0, 3.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(0.0, 3.0)
                self.histogram_2.add(4.0)
                self.histogram_2.add(2.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s maximum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(4.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.0, 0.0, 1.0, 3.0, 0.0, 2.0, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s range is partially below the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(-3.0, 2.0)
                self.histogram_1.add(1.0)
                self.histogram_1.add(-5.0, 3.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(-2.0, 3.0)
                self.histogram_2.add(4.0)
                self.histogram_2.add(2.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s maximum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(4.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s range contains the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(4.0, 2.0)
                self.histogram_1.add(1.0)
                self.histogram_1.add(-5.0, 3.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(-2.0, 3.0)
                self.histogram_2.add(-3.0)
                self.histogram_2.add(2.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the same width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have the same upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.2, 1.8, 0.0, 0.0, 1.0, 2.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s range is part of the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(-2.0, 3.0)
                self.histogram_1.add(-3.0)
                self.histogram_1.add(2.0, 2.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(4.0, 2.0)
                self.histogram_2.add(1.0)
                self.histogram_2.add(-5.0, 3.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(-5.0))
            
            with it('should have the latter\'s maximum value as the maximum value.'):
                expect(self.histogram_1.max).to(equal(4.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.2, 1.8, 0.0, 0.0, 1.0, 2.0, 0.0, 2.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s range is partially above the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(-2.0, 3.0)
                self.histogram_1.add(4.0)
                self.histogram_1.add(2.0, 2.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(-3.0, 2.0)
                self.histogram_2.add(1.0)
                self.histogram_2.add(-5.0, 3.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(-5.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.0, 3.0, 0.0, 0.0, 1.0, 2.0, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2

        with context('and the former\'s range is absolutely above the latter\'s range,' ):

            with before.all:
                self.histogram_1 = Histogram()
                self.histogram_1.add(-3.0, 2.0)
                self.histogram_1.add(-1.0)
                self.histogram_1.add(-5.0, 3.0)

                self.histogram_2 = Histogram()
                self.histogram_2.add(0.0, 3.0)
                self.histogram_2.add(4.0)
                self.histogram_2.add(2.0, 2.0)

                self.histogram_1.merge(self.histogram_2)
            
            with it('should have the latter\'s minimum value as the minimum value.'):
                expect(self.histogram_1.min).to(equal(-5.0))
            
            with it('should have an updated width for each bar.'):
                expect(self.histogram_1.width).to(equal(0.9))
            
            with it('should have an updated upper bound for each bar.'):
                upper_bounds = [round(upper_bound, 1) for upper_bound in self.histogram_1.upper_bounds]
                expect(upper_bounds).to(equal([-4.1, -3.2, -2.3, -1.4, -0.5, 0.4, 1.3, 2.2, 3.1, 4.0]))
            
            with it('should have the updated heights.'):
                heights = [round(height, 1) for height in self.histogram_1.heights]
                expect(heights).to(equal([3.0, 0.0, 2.0, 0.0, 1.0, 3.0, 0.0, 2.0, 0.0, 1.0]))
            
            with after.all:
                del self.histogram_1
                del self.histogram_2
