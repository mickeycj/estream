from estream.fading_cluster import FadingCluster

class EStream:
    
    """
    Constructor
    """
    def __init__(self,
                 max_clusters=10,
                 stream_speed=10, decay_rate=0.1, remove_threshold=0.1,
                 merge_threshold=1.25,
                 active_threshold=5.0):
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
        if not self.__is_initialized:
            self.__initialize(vector)
        else:
            self.__cluster(vector)

    def __initialize(self, vector):
        self.__clusters.append(FadingCluster(vector))

        self.__is_initialized = True
    
    def __cluster(self, vector):
        self.__fade_all()
        self.__try_split()
        self.__try_merge()
        self.__limit_clusters()
        self.__update_clusters()
        self.__add(vector)
    
    def __fade_all(self):
        for cluster in self.__clusters:
            cluster.fade(self.fading_factor)
    
    def __try_split(self):
        for cluster in self.active_clusters:
            split_index, split_attr = cluster.can_split()
            if split_index != -1 and split_attr != -1:
                self.__clusters.append(cluster.split(split_index, split_attr))
    
    def __try_merge(self):
        for idx, cluster_1 in enumerate(self.active_clusters):
            next_idx = idx + 1
            for cluster_2 in self.active_clusters[next_idx:]:
                if cluster_1.is_overlapped(cluster_2, self.merge_threshold):
                    test_cluster = FadingCluster.from_fading_cluster(cluster_1)
                    test_cluster.merge(cluster_2)

                    split_index, split_attr = test_cluster.can_split()
                    if split_index == -1 and split_attr == -1:
                        cluster_1.merge(cluster_2)
                        self.__clusters.remove(cluster_2)
    
    def __limit_clusters(self):
        pass
    
    def __update_clusters(self):
        pass
    
    def __add(self, vector):
        pass
