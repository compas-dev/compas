# type: ignore

from compas_viewer import Viewer

from compas.colors import Color
from compas.geometry import Circle
from compas.geometry import Frame

viewer = Viewer(show_grid=False)

colors = [
    Color.red(),
    Color.orange(),
    Color.yellow(),
    Color.lime(),
    Color.green(),
    Color.mint(),
    Color.cyan(),
    Color.azure(),
    Color.blue(),
    Color.violet(),
    Color.magenta(),
    Color.pink(),
]

for up in range(5):
    for right, color in enumerate(colors):
        viewer.scene.add(Circle(0.4, Frame([right, up, 0])), linecolor=color.darkened(up * 25), n=100)

for down in range(1, 5):
    for right, color in enumerate(colors):
        viewer.scene.add(Circle(0.4, Frame([right, -down, 0])), linecolor=color.lightened(down * 25), n=100)

viewer.show()
