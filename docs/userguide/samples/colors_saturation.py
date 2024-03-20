# type: ignore

from compas.geometry import Circle, Frame
from compas.colors import Color
from compas_viewer import Viewer

viewer = Viewer(show_grid = False)

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

for up in range(11):
    for right, color in enumerate(colors):
        viewer.scene.add(Circle(0.4, Frame([right, up, 0])), linecolor=color.desaturated(up * 10), n=100)

viewer.show()
