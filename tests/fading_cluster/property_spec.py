from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

from tests.utils import add_vector

with description('Fading Cluster:') as self:

    """
    Property operations
    """
    with context('When accessing fading cluster\'s center'):

        with context('and the fading cluster contains one element,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
            
            with it('should return the only element as the center.'):
                center = [round(value, 1) for value in self.fading_cluster.center]

                expect(center).to(equal([-1.5, 2.0]))
            
            with after.all:
                del self.fading_cluster

        with context('and the fading cluster contains five elements,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
                add_vector(self.fading_cluster, [-1.0, 2.0])
                add_vector(self.fading_cluster, [-1.5, 1.5])
                add_vector(self.fading_cluster, [-2.0, 1.0])
                add_vector(self.fading_cluster, [-2.0, 2.0])
            
            with it('should return the estimated center of the five elements.'):
                center = [round(value, 1) for value in self.fading_cluster.center]

                expect(center).to(equal([-1.6, 1.7]))
            
            with after.all:
                del self.fading_cluster
    
    with context('When accessing fading cluster\'s standard deviation'):

        with context('and the fading cluster has one element,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
            
            with it('should return the standard deviation of 0 for each dimension.'):
                sd = [round(value, 1) for value in self.fading_cluster.sd]

                expect(sd).to(equal([0.0, 0.0]))
            
            with after.all:
                del self.fading_cluster

        with context('and the fading cluster has five elements,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
                add_vector(self.fading_cluster, [-1.0, 2.0])
                add_vector(self.fading_cluster, [-1.5, 1.5])
                add_vector(self.fading_cluster, [-2.0, 1.0])
                add_vector(self.fading_cluster, [-2.0, 2.0])
            
            with it('should return the estimated standard deviation of the five elements for each dimension.'):
                sd = [round(value, 1) for value in self.fading_cluster.sd]

                expect(sd).to(equal([0.4, 0.4]))
            
            with after.all:
                del self.fading_cluster
