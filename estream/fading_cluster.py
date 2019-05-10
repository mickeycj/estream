from copy import deepcopy
from math import sqrt

from estream.histogram import Histogram

class FadingCluster:

    """
    ID counter
    """
    id_counter = 0

    """
    Class method
    """
    @classmethod
    def from_fading_cluster(cls, other):
        new = deepcopy(other)
        new.id = FadingCluster.id_counter
        FadingCluster.id_counter += 1

        return new

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
        if split_index == -1 or split_attribute == -1:
            return None

        lower_weight, higher_weight = 0.0, 0.0
        for idx, height in enumerate(self.histograms[split_attribute].heights):
            if idx <= split_index:
                lower_weight += height
            else:
                higher_weight += height
        if lower_weight > higher_weight:
            lower_weight, higher_weight = higher_weight, lower_weight
        
        new_fading_cluster = FadingCluster.from_fading_cluster(self)
        lower_factor, higher_factor = lower_weight / self.weight, higher_weight / self.weight
        for idx in range(self.dimension):
            if idx == split_attribute:
                new_fading_cluster.histograms[idx] = self.histograms[idx].split(split_index)

                histogram = self.histograms[idx]
                new_histogram = new_fading_cluster.histograms[idx]

                self.LS[idx], self.SS[idx] = 0.0, 0.0
                new_fading_cluster.LS[idx], new_fading_cluster.SS[idx] = 0.0, 0.0
                half_width, new_half_width = histogram.width * 0.5, new_histogram.width * 0.5
                for height, upper_bound, new_height, new_upper_bound in zip(histogram.heights,
                                                                            histogram.upper_bounds,
                                                                            new_histogram.heights,
                                                                            new_histogram.upper_bounds):
                    position = upper_bound - half_width
                    self.LS[idx] += height * position
                    self.SS[idx] += height * position ** 2

                    new_position = new_upper_bound - new_half_width
                    new_fading_cluster.LS[idx] += new_height * new_position
                    new_fading_cluster.SS[idx] += new_height * new_position ** 2
            else:
                self.LS[idx] *= higher_factor
                self.SS[idx] *= higher_factor
                self.histograms[idx].heights = [height * higher_factor for height
                                                in self.histograms[idx].heights] 
                new_fading_cluster.LS[idx] *= lower_factor
                new_fading_cluster.SS[idx] *= lower_factor
                new_fading_cluster.histograms[idx].heights = [height * lower_factor for height
                                                              in new_fading_cluster.histograms[idx].heights]
        self.weight = higher_weight
        new_fading_cluster.weight = lower_weight    

        return new_fading_cluster
    
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
