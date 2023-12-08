# type: ignore

from compas.geometry import Box, Circle, Frame
from compas.colors import Color, ColorMap
from compas_view2.app import App

viewer = App()
viewer.view.show_grid = False

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
        viewer.add(Circle(0.4, Frame([right, up, 0])).to_polygon(n=100), facecolor=color.darkened(up * 25))

for down in range(1, 5):
    for right, color in enumerate(colors):
        viewer.add(Circle(0.4, Frame([right, -down, 0])).to_polygon(n=100), facecolor=color.lightened(down * 25))

viewer.run()
