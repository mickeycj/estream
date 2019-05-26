from expects import be_none, equal, expect
from mamba import after, before, context, description, it

from estream import FadingCluster

from tests.utils import add_vector

with description('Fading Cluster:') as self:

    """
    Splitting operation
    """
    with context('When splitting the fading cluster'):

        with context('and invalid indices are given,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([2.0, 1.0])
                add_vector(self.fading_cluster, [2.0, 1.0])
                add_vector(self.fading_cluster, [2.0, 1.0])
                add_vector(self.fading_cluster, [2.0, 1.0])
                add_vector(self.fading_cluster, [2.0, 1.0])
                
                self.new_fading_cluster = self.fading_cluster.split(-1, -1)
            
            with it('should not return any new fading cluster.'):
                expect(self.new_fading_cluster).to(be_none)
            
            with after.all:
                del self.fading_cluster
                del self.new_fading_cluster

        with context('and valid indices are given,'):

            with before.all:
                FadingCluster.id_counter = 0

                self.fading_cluster = FadingCluster([-5.0, 1.0])
                for _ in range(11):
                    add_vector(self.fading_cluster, [-5.0, 1.0])
                for _ in range(9):
                    add_vector(self.fading_cluster, [-4.5, 1.0])
                for _ in range(11):
                    add_vector(self.fading_cluster, [-3.5, 1.0])
                for _ in range(10):
                    add_vector(self.fading_cluster, [-2.5, 1.0])
                for _ in range(12):
                    add_vector(self.fading_cluster, [-1.0, 1.0])
                for _ in range(2):
                    add_vector(self.fading_cluster, [0.5, 1.0])
                for _ in range(2):
                    add_vector(self.fading_cluster, [1.0, 1.0])
                for _ in range(11):
                    add_vector(self.fading_cluster, [2.0, 1.0])
                for _ in range(10):
                    add_vector(self.fading_cluster, [3.5, 1.0])
                for _ in range(11):
                    add_vector(self.fading_cluster, [4.0, 1.0])
                
                self.new_fading_cluster = self.fading_cluster.split(5, 0)
            
            with it('should have the updated weight for the original fading cluster'):
                expect(round(self.fading_cluster.weight, 1)).to(equal(30.4))
            
            with it('should have the updated LS for the original fading cluster.'):
                LS = [round(ls, 1) for ls in self.fading_cluster.LS]

                expect(LS).to(equal([-88.5, 30.4]))
            
            with it('should have the updated SS for the original fading cluster.'):
                SS = [round(ss, 1) for ss in self.fading_cluster.SS]

                expect(SS).to(equal([323.7, 30.4]))
            
            with it('should have the updated histogram at the split attribute for the original fading cluster.'):
                heights = [round(height, 1) for height in self.fading_cluster.histograms[0].heights]

                expect(heights).to(equal([5.6, 4.9, 3.4, 3.1, 2.9, 2.6, 2.6, 2.7, 1.6, 1.0]))
            
            with it('should have the updated histogram at the other attribute for the original fading cluster.'):
                heights = [round(height, 1) for height in self.fading_cluster.histograms[1].heights]

                expect(heights).to(equal([30.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
            with it('should have the weight for the new fading cluster'):
                expect(round(self.new_fading_cluster.weight, 1)).to(equal(29.1))
            
            with it('should have the LS for the new fading cluster.'):
                LS = [round(ls, 1) for ls in self.new_fading_cluster.LS]

                expect(LS).to(equal([78.7, 29.1]))
            
            with it('should have the SS for the new fading cluster.'):
                SS = [round(ss, 1) for ss in self.new_fading_cluster.SS]

                expect(SS).to(equal([242.3, 29.1]))
            
            with it('should have the histogram at the split attribute for the new fading cluster.'):
                heights = [round(height, 1) for height in self.new_fading_cluster.histograms[0].heights]

                expect(heights).to(equal([1.5, 1.5, 1.8, 2.0, 2.0, 2.3, 2.3, 4.1, 5.8, 5.8]))
            
            with it('should have the histogram at the other attribute for the new fading cluster.'):
                heights = [round(height, 1) for height in self.new_fading_cluster.histograms[1].heights]
                
                expect(heights).to(equal([29.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
            with after.all:
                del self.fading_cluster
                del self.new_fading_cluster
