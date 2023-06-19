import random
from compas.geometry import Pointcloud
from compas.utilities import i_to_rgb

from compas_plotters import Plotter

pointcloud = Pointcloud.from_bounds(8, 5, 0, 10)

plotter = Plotter(figsize=(8, 5))
for point in pointcloud:
    plotter.add(
        point,
        size=random.randint(1, 10),
        edgecolor=i_to_rgb(random.random(), normalize=True),
    )
plotter.zoom_extents()
plotter.show()
# plotter.save('docs/_images/tutorial/plotters_point-options.png', dpi=300)
