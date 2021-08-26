import compas
from compas.geometry import Point, Sphere, Box, Frame
from compas.datastructures import Mesh

import compas_rhino
from compas_rhino.scene import Scene

compas_rhino.clear()

scene = Scene()

scene.add(Sphere(Point(1.5, 1.5, 1.5), 1.0))
scene.add(Box(Frame.worldXY(), 3, 3, 3))
scene.add(Mesh.from_obj(compas.get('tubemesh.obj')))

scene.update()
