import random
from compas.geometry import Line
from compas.geometry import Pointcloud
from compas.utilities import i_to_rgb, grouper

from compas_plotters import Plotter

plotter = Plotter(figsize=(8, 5))

pointcloud = Pointcloud.from_bounds(8, 5, 0, 10)

for a, b in grouper(pointcloud, 2):
    line = Line(a, b)
    plotter.add(
        line,
        linewidth=2.0,
        linestyle=random.choice(["dotted", "dashed", "solid"]),
        color=i_to_rgb(random.random(), normalize=True),
        draw_points=True,
    )

plotter.zoom_extents()
plotter.show()
# plotter.save('docs/_images/tutorial/plotters_line-options.png', dpi=300)
