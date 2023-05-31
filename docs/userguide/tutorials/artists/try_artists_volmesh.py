from compas.datastructures import VolMesh
from compas.artists import Artist
from compas.colors import Color

mesh = VolMesh.from_meshgrid(dx=10, nx=10)

Artist.clear()

artist = Artist(mesh)
artist.draw_cells(color={cell: Color.pink() for cell in mesh.cell_sample(size=83)})

Artist.redraw()
