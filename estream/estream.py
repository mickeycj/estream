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
        self.__is_initialized = False
    
    """
    Properties
    """
    @property
    def clusters(self):
        return [cluster for cluster in self.__clusters]
    
    @property
    def active_clusters(self):
        return [cluster for cluster in self.__clusters if cluster.is_active]
    
    @property
    def inactive_clusters(self):
        return [cluster for cluster in self.__clusters if not cluster.is_active]
    
    @property
    def num_clusters(self):
        return sum(cluster.is_active for cluster in self.__clusters)
    
    """
    Public method
    """
    def fit(self, X):
        for vector in X:
            self.__fit_vector(vector)
        
        return self.active_clusters
    
    """
    Private methods
    """
    def __fit_vector(self, vector):
        if self.__is_initialized:
            self.__initialize(vector)
        else:
            self.__cluster(vector)

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
