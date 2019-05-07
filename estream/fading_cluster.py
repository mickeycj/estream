from copy import deepcopy

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
    Public methods
    """
    def center(self):
        pass
    
    def sd(self):
        pass
    
    def get_center_distance(self, other):
        pass
    
    def get_normalized_distance(self, vector):
        pass
    
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
