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
    Properties
    """
    @property
    def center(self):
        return [value / self.weight for value in self.LS]

    @property    
    def sd(self):
        def __compute_sd(ls, ss):
            sd = ss / self.weight -(ls / self.weight) ** 2

            return sqrt(sd) if sd >= 0.00001 else 0.00001
        
        return [__compute_sd(ls, ss) for ls, ss in zip(self.LS, self.SS)]
    
    """
    Public methods
    """
    def get_center_distance(self, other):
        return sum([abs(center - other_center) for center, other_center
                    in zip(self.center, other.center)]) / self.dimension
    
    def get_normalized_distance(self, vector):
        return sum([abs(center - value) / sd for center, value, sd
                    in zip(self.center, vector, self.sd)]) / self.dimension
    
    def is_overlapped(self, other, merge_threshold):
        return sum([abs(center - other_center) - merge_threshold * (sd + other_sd)
                    for center, other_center, sd, other_sd
                    in zip(self.center, other.center, self.sd, other.sd)]) / self.dimension <= 1
    
    def fade(self, fading_factor):
        self.weight *= fading_factor
        self.LS = [ls * fading_factor for ls in self.LS]
        self.SS = [ss * fading_factor for ss in self.SS]
        for histogram in self.histograms:
            histogram.heights = [height * fading_factor for height in histogram.heights]
    
    def can_split(self):
        for split_attribute, histogram in enumerate(self.histograms):
            split_index = histogram.find_split_index()
            if split_index != -1:
                return split_index, split_attribute
        
        return -1, -1
    
    def split(self, split_index, split_attribute):
        pass
    
    def merge(self, other):
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
