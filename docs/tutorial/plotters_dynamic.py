from compas.geometry import Pointcloud, Translation
from compas.utilities import i_to_red, pairwise

from compas_plotters import Plotter

plotter = Plotter(figsize=(8, 5))

pointcloud = Pointcloud.from_bounds(8, 5, 0, 10)

for index, (a, b) in enumerate(pairwise(pointcloud)):
    artist = plotter.add(a, edgecolor=i_to_red(max(index / 10, 0.1), normalize=True))

plotter.add(b, size=10, edgecolor=(1, 0, 0))
plotter.zoom_extents()
plotter.pause(1.0)


@plotter.on(
    interval=0.1,
    frames=50,
    record=True,
    recording="docs/_images/tutorial/plotters_dynamic.gif",
    dpi=150,
)
def move(frame):
    print(frame)
    for a, b in pairwise(pointcloud):
        vector = b - a
        a.transform(Translation.from_vector(vector * 0.1))


plotter.show()
