""""""

from __future__ import print_function
from __future__ import division

from numpy import asarray
from numpy import argmin
from numpy import argpartition
from scipy.spatial import distance_matrix


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [

]


def closest_points_in_cloud_numpy(points, cloud, threshold=10**7, distances=True, num_nbrs=1):
    """Find the closest points in a point cloud to a set of sample points.

    Note:
        Items in cloud further from items in points than threshold return zero
        distance and will affect the indices returned if not set suitably high.

    Parameters:
        points (array, list): The sample points (n,).
        cloud (array, list): The cloud points to compare to (n,).
        threshold (float): Points are checked within this distance.
        distances (boolean): Return distance matrix.

    Returns:
        list: Indices of the closest points in the cloud per point in points.
        array: Distances between points and closest points in cloud (n x n).

    Examples:
        >>> a = np.random.rand(4, 3)
        >>> b = np.random.rand(4, 3)
        >>> indices, distances = closest_points(a, b, distances=True)
        [1, 2, 0, 3]
        array([[ 1.03821946,  0.66226402,  0.67964346,  0.98877891],
               [ 0.4650432 ,  0.54484186,  0.36158995,  0.60385484],
               [ 0.19562088,  0.73240154,  0.50235761,  0.51439644],
               [ 0.84680233,  0.85390316,  0.72154983,  0.50432293]])
    """
    points = asarray(points).reshape((-1, 3))
    cloud = asarray(cloud).reshape((-1, 3))
    d_matrix = distance_matrix(points, cloud, threshold=threshold)
    if num_nbrs == 1:
        indices = argmin(d_matrix, axis=1)
    else:
        indices = argpartition(d_matrix, num_nbrs, axis=1)
    if distances:
        return indices, d_matrix
    return indices


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
