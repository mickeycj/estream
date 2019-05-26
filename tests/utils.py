"""
Mocked fading factor
"""
fading_factor = 0.99

"""
Mocked method for adding vectors
"""
def add_vector(cluster, vector):
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
