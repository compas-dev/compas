from compas.datastructures import CellNetwork
file = "/Users/romanarust/workspace/compas_dev/compas/docs/userguide/network.json"

network = CellNetwork.from_json(file)

from compas.geometry import Polygon

#import compas_view2

#print(compas_view2.__file__)
#from compas_view2.app import App

def show(cell_network):


    viewer = App()

    opacity = 0.5

    for face in cell_network.faces_on_boundaries():
        vertices = cell_network.face_coordinates(face)
        viewer.add(Polygon(vertices), facecolor=[0.75, 0.75, 0.75], opacity=opacity)

    for face in cell_network.faces_no_cell():
        vertices = cell_network.face_coordinates(face)
        viewer.add(Polygon(vertices), facecolor=[0.5, 0.55, 1.0], opacity=opacity)

    for face in cell_network.faces():
        cells = cell_network.face_cells(face)
        vertices = cell_network.face_coordinates(face)

        if not len(cells):
            pass
            # viewer.add(Polygon(vertices), facecolor=[0.5, 0.55, 1.0], opacity=opacity)

        elif len(cells) == 2:
            pass
            # viewer.add(Polygon(vertices), facecolor=[1, 0.8, 0.05], opacity=opacity)
        # break

    viewer.add(cell_network.to_network(), show_lines=True)
    viewer.view.camera.zoom_extents()
    viewer.show()

#show(network)


from compas.scene import Scene



scene = Scene()
scene.clear()
#scene.add(network)
opacity = 0.5
cell_network = network

for face in cell_network.faces_on_boundaries():
    vertices = cell_network.face_coordinates(face)
    scene.add(Polygon(vertices), facecolor=[0.75, 0.75, 0.75], opacity=opacity)

scene.draw()
