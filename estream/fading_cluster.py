from copy import deepcopy
from math import sqrt

from estream.histogram import Histogram

class FadingCluster:

    """
    ID counter
    """
    id_counter = 0

    """
    Constructor
    """
    def __init__(self, vector):
        # Cluster ID
        self.id = FadingCluster.id_counter
        FadingCluster.id_counter += 1
        # Public fields
        self.is_active = False
        self.weight = 1.0
        self.dimension = len(vector)
        self.LS = [value for value in vector]
        self.SS = [value ** 2 for value in vector]
        self.histograms = []
        for value in vector:
            histogram = Histogram()
            histogram.add(value)
            self.histograms.append(histogram)
    
    """
    Overridden methods
    """
    def __copy__(self):
        return self.__clone()
    
    def __deepcopy__(self, memo):
        copy = self.__clone()
        copy.LS = deepcopy(self.LS)
        copy.SS = deepcopy(self.SS)
        copy.histograms = deepcopy(self.histograms)

        return copy
    
    """
    Accessor methods
    """
    def get_center(self):
        return [value / self.weight for value in self.LS]
    
    def get_sd(self):
        def __compute_sd(ls, ss):
            sd = ss / self.weight -(ls / self.weight) ** 2

            return sqrt(sd) if sd >= 0.00001 else 0.00001
        
        return [__compute_sd(ls, ss) for ls, ss in zip(self.LS, self.SS)]
    
    """
    Public methods
    """
    def get_center_distance(self, other):
        return sum([abs(center - other_center) for center, other_center
                    in zip(self.get_center(), other.get_center())]) / self.dimension
    
    def get_normalized_distance(self, vector):
        return sum([abs(center - value) / sd for center, value, sd
                    in zip(self.get_center(), vector, self.get_sd())]) / self.dimension
    
    def fade(self, fading_factor):
        pass
    
    def can_split(self):
        pass
    
    def split(self):
        pass
    
    def merge(self, other):
        pass
    
    def is_overlapped(self, other, threshold):
        pass
    
    def add(self, vector):
        pass
    
    """
    Private methods
    """
    def __clone(self):
        cls = self.__class__
        clone = cls.__new__(cls)
        clone.__dict__.update(self.__dict__)

        return clone
