from numpy import random

import matplotlib.pyplot as plt

from compas.numerical.xforms import rotation_matrix
from compas.numerical.transformations import transform

from compas.visualization.plotters.core.helpers import Axes3D
from compas.visualization.plotters.core.helpers import Cloud3D
from compas.visualization.plotters.core.helpers import Bounds
from compas.visualization.plotters.core.drawing import create_axes_3d

from compas.numerical.statistics import principal_components

data = random.rand(300, 3)
data[:, 0] *= 10.0
data[:, 1] *= 1.0
data[:, 2] *= 4.0

a = 3.14159 * 30.0 / 180
Ry = rotation_matrix(a, [0, 1.0, 0.0])

a = -3.14159 * 45.0 / 180
Rz = rotation_matrix(a, [0, 0, 1.0])

R = Rz.dot(Ry)

data = transform(data, R)

average, vectors, values = principal_components(data)

axes = create_axes_3d()

Bounds(data).plot(axes)
Cloud3D(data).plot(axes)
Axes3D(average, vectors).plot(axes)

plt.show()