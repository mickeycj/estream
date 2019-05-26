from expects import be_false, be_true, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

from tests.utils import add_vector

with description('E-Stream:') as self:

    """
    Clusters updating operation
    """
    with context('When updating clusters,'):

        with before.all:
            FadingCluster.id_counter = 0

            cluster_1 = FadingCluster([-3.0, 4.0])
            add_vector(cluster_1, [-2.0, 4.0])
            add_vector(cluster_1, [-3.0, 3.0])
            add_vector(cluster_1, [-4.0, 2.0])
            add_vector(cluster_1, [-4.0, 4.0])

            cluster_2 = FadingCluster([1.5, 2.0])
            add_vector(cluster_2, [-1.0, 2.0])
            add_vector(cluster_2, [-1.5, 1.5])
            add_vector(cluster_2, [-2.0, 1.0])
            add_vector(cluster_2, [2.0, 2.0])
            add_vector(cluster_2, [-3.0, 3.0])

            cluster_3 = FadingCluster([3.0, -4.0])
            add_vector(cluster_3, [2.0, -4.0])
            add_vector(cluster_3, [3.0, -3.0])
            add_vector(cluster_3, [4.0, -2.0])
            add_vector(cluster_3, [4.0, -4.0])

            cluster_4 = FadingCluster([0.5, 2.0])
            add_vector(cluster_4, [-1.0, 1.0])
            add_vector(cluster_4, [0.5, 1.5])
            add_vector(cluster_4, [0.0, 2.0])
            add_vector(cluster_4, [2.0, 2.0])
            add_vector(cluster_4, [-2.0, 4.0])

            self.estream = EStream()
            self.estream._EStream__clusters = [cluster_1, cluster_2, cluster_3, cluster_4]

            self.estream._EStream__update_clusters()
        
        with it('should have an upated state of each cluster.'):
            expect(self.estream.clusters[0].is_active).to(be_false)
            expect(self.estream.clusters[1].is_active).to(be_true)
            expect(self.estream.clusters[2].is_active).to(be_false)
            expect(self.estream.clusters[3].is_active).to(be_true)
        
        with after.all:
            del self.estream