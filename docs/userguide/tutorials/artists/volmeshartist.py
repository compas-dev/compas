from compas.datastructures import VolMesh
from compas.scene import SceneObject
from compas.colors import Color

mesh = VolMesh.from_meshgrid(dx=10, nx=10)

SceneObject.clear()

artist = SceneObject(mesh)
artist.draw_cells(color={cell: Color.pink() for cell in mesh.cell_sample(size=83)})

SceneObject.redraw()
