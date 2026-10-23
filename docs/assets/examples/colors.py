# type: ignore

from compas_viewer import Viewer

from compas.colors import Color
from compas.geometry import Circle
from compas.geometry import Frame

viewer = Viewer(show_grid=False)

viewer.scene.add(Circle(0.4, Frame([0, 0, 0])), linecolor=Color.red(), n=100)
viewer.scene.add(Circle(0.4, Frame([1, 0, 0])), linecolor=Color.orange(), n=100)
viewer.scene.add(Circle(0.4, Frame([2, 0, 0])), linecolor=Color.yellow(), n=100)
viewer.scene.add(Circle(0.4, Frame([3, 0, 0])), linecolor=Color.lime(), n=100)
viewer.scene.add(Circle(0.4, Frame([4, 0, 0])), linecolor=Color.green(), n=100)
viewer.scene.add(Circle(0.4, Frame([5, 0, 0])), linecolor=Color.mint(), n=100)
viewer.scene.add(Circle(0.4, Frame([6, 0, 0])), linecolor=Color.cyan(), n=100)
viewer.scene.add(Circle(0.4, Frame([7, 0, 0])), linecolor=Color.azure(), n=100)
viewer.scene.add(Circle(0.4, Frame([8, 0, 0])), linecolor=Color.blue(), n=100)
viewer.scene.add(Circle(0.4, Frame([9, 0, 0])), linecolor=Color.violet(), n=100)
viewer.scene.add(Circle(0.4, Frame([10, 0, 0])), linecolor=Color.magenta(), n=100)
viewer.scene.add(Circle(0.4, Frame([11, 0, 0])), linecolor=Color.pink(), n=100)
viewer.scene.add(Circle(0.4, Frame([12, 0, 0])), linecolor=Color.red(), n=100)

viewer.show()
