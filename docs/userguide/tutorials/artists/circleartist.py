from compas.geometry import Circle
from compas.artists import Artist

Artist.clear()

circle = Circle(radius=3.0)

artist = Artist(circle)
artist.draw(color=(0.0, 0.0, 1.0), show_point=True, show_normal=True)

Artist.redraw()
