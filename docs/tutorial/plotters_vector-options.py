from compas.geometry import Pointcloud
from compas.utilities import i_to_red, pairwise

from compas_plotters import Plotter

plotter = Plotter(figsize=(8, 5))

pointcloud = Pointcloud.from_bounds(8, 5, 0, 10)

for index, (a, b) in enumerate(pairwise(pointcloud)):
    vector = b - a
    vector.unitize()
    plotter.add(
        vector,
        point=a,
        draw_point=True,
        color=i_to_red(max(index / 10, 0.1), normalize=True),
    )

plotter.add(b, size=10, edgecolor=(1, 0, 0))

plotter.zoom_extents()
plotter.show()
plotter.save("docs/_images/tutorial/plotters_vector-options.png", dpi=300)
