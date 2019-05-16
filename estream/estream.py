class EStream:
    
    """
    Constructor
    """
    def __init__(self,
                 max_clusters=10,
                 stream_speed=10, decay_rate=0.1, remove_threshold=0.1,
                 merge_threshold=1.25,
                 active_threshold=5):
        # Public fields
        self.max_clusters = max_clusters
        self.fading_factor = 2 ** (-decay_rate * (1 / stream_speed))
        self.remove_threshold = remove_threshold
        self.merge_threshold = merge_threshold
        self.active_threshold = active_threshold
        # Private fields
        self.__clusters = []
        self.__initialized = False
    
    """
    Properties
    """
    @property
    def num_clusters(self):
        pass

    @property
    def clusters(self):
        pass
    
    @property
    def active_clusters(self):
        pass
    
    @property
    def inactive_clusters(self):
        pass
    
    """
    Public method
    """
    def fit(self, X):
        pass
    
    """
    Private methods
    """
    def __fit_vector(self, vector):
        pass

    def __initialize(self, vector):
        pass
    
    def __cluster(self, vector):
        pass
    
    def __fade_all(self):
        pass
    
    def __try_split(self):
        pass
    
    def __try_merge(self):
        pass
    
    def __limit_clusters(self):
        pass
    
    def __update_clusters(self):
        pass
    
    def __add(self, vector):
        pass
