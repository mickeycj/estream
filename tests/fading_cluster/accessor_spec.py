from expects import equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

with description('Fading Cluster:') as self:

    def add(self, cluster, vector):
        fading_factor = 0.9

        cluster.weight *= fading_factor
        cluster.LS = [ls * fading_factor for ls in cluster.LS]
        cluster.SS = [ss * fading_factor for ss in cluster.SS]
        for histogram in cluster.histograms:
            histogram.heights = [height * fading_factor for height in histogram.heights]

        cluster.weight += 1.0
        cluster.LS = [ls + value for ls, value in zip(cluster.LS, vector)]
        cluster.SS = [ss + value ** 2 for ss, value in zip(cluster.SS, vector)]
        for histogram, value in zip(cluster.histograms, vector):
            histogram.add(value)

    with context('When accessing fading cluster\'s center'):

        with context('and the fading cluster contains one element,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
                
                self.center = self.fading_cluster.get_center()
            
            with it('should return the only element as the center.'):
                center = [round(value, 1) for value in self.center]
                expect(center).to(equal([-1.5, 2.0]))
            
            with after.all:
                del self.fading_cluster
                del self.center

        with context('and the fading cluster contains five elements,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
                self.add(self.fading_cluster, [-1.0, 2.0])
                self.add(self.fading_cluster, [-1.5, 1.5])
                self.add(self.fading_cluster, [-2.0, 1.0])
                self.add(self.fading_cluster, [-2.0, 2.0])

                self.center = self.fading_cluster.get_center()
            
            with it('should return the estimated center of the five elements.'):
                center = [round(value, 1) for value in self.center]
                expect(center).to(equal([-1.6, 1.7]))
            
            with after.all:
                del self.fading_cluster
                del self.center
    
    with context('When accessing fading cluster\'s standard deviation'):

        with context('and the fading cluster has one element,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fadiing_cluster = FadingCluster([-1.5, 2.0])

                self.sd = self.fadiing_cluster.get_sd()
            
            with it('should return the standard deviation of 0 for each dimension.'):
                sd = [round(value, 1) for value in self.sd]
                expect(sd).to(equal([0.0, 0.0]))
            
            with after.all:
                del self.fadiing_cluster
                del self.sd

        with context('and the fading cluster has five elements,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-1.5, 2.0])
                self.add(self.fading_cluster, [-1.0, 2.0])
                self.add(self.fading_cluster, [-1.5, 1.5])
                self.add(self.fading_cluster, [-2.0, 1.0])
                self.add(self.fading_cluster, [-2.0, 2.0])

                self.sd = self.fading_cluster.get_sd()
            
            with it('should return the estimated standard deviation of the five elements for each dimension.'):
                sd = [round(value, 1) for value in self.sd]
                expect(sd).to(equal([0.4, 0.4]))
            
            with after.all:
                del self.fading_cluster
                del self.sd
