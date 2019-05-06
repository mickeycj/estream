from expects import equal, expect
from mamba import after, before, context, description, it

from estream import Histogram

with description('Histogram:') as self:

    """
    Finding split index operation
    """
    with context('When finding split index in a histogram'):

        with context('that does not have any valley,'):

            with before.all:
                self.histogram = Histogram()
                self.histogram.add(1.0)
                self.histogram.add(2.0)
                self.histogram.add(3.0)

                self.split_index = self.histogram.find_split_index()
            
            with it('should return the split index of -1.'):
                expect(self.split_index).to(equal(-1))
            
            with after.all:
                del self.histogram
                del self.split_index
        
        with context('that has one valley,'):

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

                self.split_index = self.histogram.find_split_index()
            
            with it('should return the split index of 5.'):
                expect(self.split_index).to(equal(5))
            
            with after.all:
                del self.histogram
                del self.split_index
        
        with context('that has two valleys'):

            with context('and the minimum valley appears first,'):

                with before.all:
                    self.histogram = Histogram()
                    self.histogram.add(-5.0, 9.0)
                    self.histogram.add(-4.5, 12.0)
                    self.histogram.add(-3.5, 4.5)
                    self.histogram.add(-2.5, 1.5)
                    self.histogram.add(-1.0)
                    self.histogram.add(0.5, 8.0)
                    self.histogram.add(1.0, 11.0)
                    self.histogram.add(2.0, 1.5)
                    self.histogram.add(3.5, 6.5)
                    self.histogram.add(4.0, 10.0)

                    self.split_index = self.histogram.find_split_index()
                
                with it('should return the split index of 3.'):
                    expect(self.split_index).to(equal(3))
                
                with after.all:
                    del self.histogram
                    del self.split_index

            with context('and the minimum valley appears last,'):

                with before.all:
                    self.histogram = Histogram()
                    self.histogram.add(-5.0, 10.0)
                    self.histogram.add(-4.5, 6.5)
                    self.histogram.add(-3.5, 1.5)
                    self.histogram.add(-2.5, 11.0)
                    self.histogram.add(-1.0, 8.0)
                    self.histogram.add(0.5)
                    self.histogram.add(1.0, 1.5)
                    self.histogram.add(2.0, 4.5)
                    self.histogram.add(3.5, 12.0)
                    self.histogram.add(4.0, 9.0)

                    self.split_index = self.histogram.find_split_index()
                
                with it('should return the split index of 5.'):
                    expect(self.split_index).to(equal(5))
                
                with after.all:
                    del self.histogram
                    del self.split_index
