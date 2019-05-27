from expects import be_false, be_true, equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

from tests.utils import add_vector

with description('Fading Cluster:') as self:

    """
    Distance operations
    """
    with context('When computing distance to another fading cluster,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster_1 = FadingCluster([-1.5, 2.0])
            add_vector(self.fading_cluster_1, [-1.0, 2.0])
            add_vector(self.fading_cluster_1, [-1.5, 1.5])
            add_vector(self.fading_cluster_1, [-2.0, 1.0])
            add_vector(self.fading_cluster_1, [-2.0, 2.0])

            self.fading_cluster_2 = FadingCluster([1.5, -2.0])
            add_vector(self.fading_cluster_2, [1.0, -2.0])
            add_vector(self.fading_cluster_2, [1.5, -1.5])
            add_vector(self.fading_cluster_2, [2.0, -1.0])
            add_vector(self.fading_cluster_2, [2.0, -2.0])

            self.distance = self.fading_cluster_1.get_center_distance(self.fading_cluster_2)
        
        with it('should return the estimated distance between the two fading clusters.'):
            expect(round(self.distance, 1)).to(equal(3.3))
        
        with after.all:
            del self.fading_cluster_1
            del self.fading_cluster_2
            del self.distance

    with context('When computing distance to another vector,'):

        with before.all:
            FadingCluster.id_counter = 0

            self.fading_cluster = FadingCluster([-1.5, 2.0])
            add_vector(self.fading_cluster, [-1.0, 2.0])
            add_vector(self.fading_cluster, [-1.5, 1.5])
            add_vector(self.fading_cluster, [-2.0, 1.0])
            add_vector(self.fading_cluster, [-2.0, 2.0])

            self.distance = self.fading_cluster.get_normalized_distance([1.6, -1.7])
        
        with it('should return the estimated distance between the fading cluster and the vector.'):
            expect(round(self.distance, 1)).to(equal(8.5))
        
        with after.all:
            del self.fading_cluster
            del self.distance
    
    with context('When computing whether two fading clusters overlap with each other'):

        with context('and they don\'t overlap,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster_1 = FadingCluster([-1.5, 2.0])
                add_vector(self.fading_cluster_1, [-1.0, 2.0])
                add_vector(self.fading_cluster_1, [-1.5, 1.5])
                add_vector(self.fading_cluster_1, [-2.0, 1.0])
                add_vector(self.fading_cluster_1, [-2.0, 2.0])

                self.fading_cluster_2 = FadingCluster([1.5, -2.0])
                add_vector(self.fading_cluster_2, [1.0, -2.0])
                add_vector(self.fading_cluster_2, [1.5, -1.5])
                add_vector(self.fading_cluster_2, [2.0, -1.0])
                add_vector(self.fading_cluster_2, [2.0, -2.0])

                self.is_overlapped = self.fading_cluster_1.is_overlapped(self.fading_cluster_2, 1.25)
            
            with it('should return false.'):
                expect(self.is_overlapped).to(be_false)
            
            with after.all:
                del self.fading_cluster_1
                del self.fading_cluster_2
                del self.is_overlapped

        with context('and they overlap,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster_1 = FadingCluster([1.5, 2.0])
                add_vector(self.fading_cluster_1, [-1.0, 2.0])
                add_vector(self.fading_cluster_1, [-1.5, 1.5])
                add_vector(self.fading_cluster_1, [-2.0, 1.0])
                add_vector(self.fading_cluster_1, [2.0, 2.0])

                self.fading_cluster_2 = FadingCluster([0.5, 2.0])
                add_vector(self.fading_cluster_2, [-1.0, 1.0])
                add_vector(self.fading_cluster_2, [0.5, 1.5])
                add_vector(self.fading_cluster_2, [0.0, 2.0])
                add_vector(self.fading_cluster_2, [2.0, 2.0])

                self.is_overlapped = self.fading_cluster_1.is_overlapped(self.fading_cluster_2, 1.25)
            
            with it('should return true.'):
                expect(self.is_overlapped).to(be_true)
            
            with after.all:
                del self.fading_cluster_1
                del self.fading_cluster_2
                del self.is_overlapped
