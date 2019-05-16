from expects import equal, expect
from mamba import after, before, context, description, it

from estream import EStream, FadingCluster

with description('E-Stream:') as self:

    """
    Property operations
    """
    with context('When requesting properties,'):

        with before.all:
            self.estream = EStream()
            self.estream._EStream__clusters = [FadingCluster([0.0, 0.0]),
                                               FadingCluster([0.0, 0.0]),
                                               FadingCluster([0.0, 0.0]),
                                               FadingCluster([0.0, 0.0]),
                                               FadingCluster([0.0, 0.0])]
            self.estream._EStream__clusters[0].is_active = True
            self.estream._EStream__clusters[2].is_active = True
            self.estream._EStream__clusters[4].is_active = True

        with it('should return all clusters.'):
            clusters = self.estream.clusters

            expect(len(clusters)).to(equal(5))
            expect([cluster.id for cluster in clusters]).to(equal([0, 1, 2, 3, 4]))
        
        with it('should return only active clusters.'):
            active_clusters = self.estream.active_clusters

            expect(len(active_clusters)).to(equal(3))
            expect([cluster.id for cluster in active_clusters]).to(equal([0, 2, 4]))
            expect(sum(cluster.is_active for cluster in active_clusters)).to(equal(3))
        
        with it('should return only inactive clusters.'):
            inactive_clusters = self.estream.inactive_clusters

            expect(len(inactive_clusters)).to(equal(2))
            expect([cluster.id for cluster in inactive_clusters]).to(equal([1, 3]))
            expect(sum(not cluster.is_active for cluster in inactive_clusters)).to(equal(2))
        
        with it('should return the number of active clusters.'):
            expect(self.estream.num_clusters).to(equal(3))
        
        with after.all:
            del self.estream
