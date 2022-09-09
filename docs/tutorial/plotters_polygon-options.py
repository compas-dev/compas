from compas.geometry import Polygon, Translation

from compas_plotters import Plotter

poly1 = Polygon.from_sides_and_radius_xy(5, 1.0)
poly2 = Polygon.from_sides_and_radius_xy(5, 1.0).transformed(
    Translation.from_vector([0.5, -0.25, 0])
)
poly3 = Polygon.from_sides_and_radius_xy(5, 1.0).transformed(
    Translation.from_vector([0.75, +0.25, 0])
)

plotter = Plotter(figsize=(8, 5))
plotter.add(poly1, linewidth=3.0, facecolor=(0.8, 1.0, 0.8), edgecolor=(0.0, 1.0, 0.0))
plotter.add(
    poly2, linestyle="dashed", facecolor=(1.0, 0.8, 0.8), edgecolor=(1.0, 0.0, 0.0)
)
plotter.add(poly3, alpha=0.5)
plotter.zoom_extents()
plotter.show()
# plotter.save('docs/_images/tutorial/plotters_polygon-options.png', dpi=300)
