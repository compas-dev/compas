# type: ignore

from compas.geometry import Box, Circle, Frame
from compas.colors import Color, ColorMap
from compas_view2.app import App

viewer = App()
viewer.view.show_grid = False

viewer.add(Circle(0.4, Frame([0, 0, 0])).to_polygon(n=100), facecolor=Color.red())
viewer.add(Circle(0.4, Frame([1, 0, 0])).to_polygon(n=100), facecolor=Color.orange())
viewer.add(Circle(0.4, Frame([2, 0, 0])).to_polygon(n=100), facecolor=Color.yellow())
viewer.add(Circle(0.4, Frame([3, 0, 0])).to_polygon(n=100), facecolor=Color.lime())
viewer.add(Circle(0.4, Frame([4, 0, 0])).to_polygon(n=100), facecolor=Color.green())
viewer.add(Circle(0.4, Frame([5, 0, 0])).to_polygon(n=100), facecolor=Color.mint())
viewer.add(Circle(0.4, Frame([6, 0, 0])).to_polygon(n=100), facecolor=Color.cyan())
viewer.add(Circle(0.4, Frame([7, 0, 0])).to_polygon(n=100), facecolor=Color.azure())
viewer.add(Circle(0.4, Frame([8, 0, 0])).to_polygon(n=100), facecolor=Color.blue())
viewer.add(Circle(0.4, Frame([9, 0, 0])).to_polygon(n=100), facecolor=Color.violet())
viewer.add(Circle(0.4, Frame([10, 0, 0])).to_polygon(n=100), facecolor=Color.magenta())
viewer.add(Circle(0.4, Frame([11, 0, 0])).to_polygon(n=100), facecolor=Color.pink())
viewer.add(Circle(0.4, Frame([12, 0, 0])).to_polygon(n=100), facecolor=Color.red())

viewer.run()
