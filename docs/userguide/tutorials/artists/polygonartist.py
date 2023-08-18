from compas.geometry import Polygon
from compas.artists import Artist

Artist.clear()

polygon = Polygon.from_sides_and_radius_xy(8, 7.0)

artist = Artist(polygon)
artist.color = (0.0, 1.0, 0.0)

artist.draw(show_points=True, show_edges=True)

Artist.redraw()
