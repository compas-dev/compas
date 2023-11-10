from compas.geometry import Polyhedron
from compas.scene import SceneObject

SceneObject.clear()

polyhedron = Polyhedron.from_platonicsolid(f=8)
artist = SceneObject(polyhedron)
artist.draw()

SceneObject.redraw()
