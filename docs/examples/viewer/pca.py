from numpy import random

import matplotlib.pyplot as plt

from compas.geometry import matrix_from_axis_and_angle
from compas.geometry import transform_points_numpy

from compas_plotters import Axes3D
from compas_plotters import Cloud3D
from compas_plotters import Bounds
from compas_plotters import create_axes_3d

from compas.numerical import pca_numpy

data = random.rand(300, 3)
data[:, 0] *= 10.0
data[:, 1] *= 1.0
data[:, 2] *= 4.0

a = 3.14159 * 30.0 / 180
Ry = matrix_from_axis_and_angle([0, 1.0, 0.0], a, rtype='array')

a = -3.14159 * 45.0 / 180
Rz = matrix_from_axis_and_angle([0, 0, 1.0], a, rtype='array')

R = Rz.dot(Ry)

data = transform_points_numpy(data, R)

average, vectors, values = pca_numpy(data)

axes = create_axes_3d()

Bounds(data).plot(axes)
Cloud3D(data).plot(axes)
Axes3D(average, vectors).plot(axes)

plt.show()
