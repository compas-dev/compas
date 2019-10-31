
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from vtk import vtkActor
    from vtk import vtkAxesActor
    from vtk import vtkCamera
    from vtk import vtkCellArray
    from vtk import vtkColorTransferFunction
    from vtk import vtkFixedPointVolumeRayCastMapper
    from vtk import vtkGlyph3DMapper
    from vtk import vtkIdList
    from vtk import vtkImageImport
    from vtk import vtkInteractorStyleTrackballCamera
    from vtk import vtkLine
    from vtk import vtkPiecewiseFunction
    from vtk import vtkPoints
    from vtk import vtkPolyData
    from vtk import vtkPolyDataMapper
    from vtk import vtkRenderer
    from vtk import vtkRenderWindow
    from vtk import vtkSphereSource
    from vtk import vtkUnsignedCharArray
    from vtk import vtkVolume
    from vtk import vtkVolumeProperty
    from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
except ImportError:
    pass

try:
    from numpy import asarray
    from numpy import max
    from numpy import min
    from numpy import uint8
except ImportError:
    pass

try:
    from PyQt5.Qt import QApplication
    from PyQt5.Qt import QCheckBox
    from PyQt5.Qt import QComboBox
    from PyQt5.Qt import QDockWidget
    from PyQt5.Qt import QFrame
    from PyQt5.Qt import QLabel
    from PyQt5.Qt import QMainWindow
    from PyQt5.Qt import QSlider
    from PyQt5.Qt import QVBoxLayout
    from PyQt5.Qt import QWidget
    from PyQt5.QtCore import Qt
except ImportError:
    pass

import sys


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VtkViewer',
]


# ==============================================================================
# MainWindow
# ==============================================================================

class MainWindow(QMainWindow):

    def __init__(self, application, parent=None):
        QMainWindow.__init__(self, parent)

        # Camera

        px, py, pz = application.camera_position
        tx, ty, tz = application.camera_target

        self.camera = camera = vtkCamera()
        camera.SetViewUp(0, 0, 1)
        camera.SetPosition(px, py, pz)
        camera.SetFocalPoint(tx, ty, tz)

        # Renderer

        self.renderer = renderer = vtkRenderer()
        renderer.SetBackground(1.0, 1.0, 1.0)
        renderer.SetBackground2(0.8, 0.8, 0.8)
        renderer.GradientBackgroundOn()
        renderer.SetActiveCamera(camera)
        renderer.ResetCamera()
        renderer.ResetCameraClippingRange()
        renderer.UseFXAAOn()

        self.window = window = vtkRenderWindow()
        window.AddRenderer(renderer)

        # Widget

        self.frame  = frame  = QFrame()
        self.widget = widget = QVTKRenderWindowInteractor(frame, rw=window)
        self.layout = layout = QVBoxLayout()
        layout.addWidget(widget)
        frame.setLayout(layout)

        # Interactor

        self.interactor = interactor = widget.GetRenderWindow().GetInteractor()
        interactor.SetInteractorStyle(InteractorStyle())
        interactor.AddObserver('KeyPressEvent', application.keypress)
        interactor.Initialize()
        interactor.Start()

        self.resize(application.width, application.height)
        self.setCentralWidget(frame)


# ==============================================================================
# Misc
# ==============================================================================

class InteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        pass


class QHLine(QFrame):

    def __init__(self):
        super(QHLine, self).__init__()

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


# ==============================================================================
# VtkViewer
# ==============================================================================

class VtkViewer(QApplication):

    def __init__(self, name='VTK Viewer', data={}, height=900, width=1440, sidebar=120, datastructure=None):
        QApplication.__init__(self, sys.argv)

        if datastructure:

            D = datastructure
            k_i = D.key_index()

            data = {}
            data['vertices'] = [D.vertex_coordinates(k_i[k]) for k in D.vertices()]
            data['edges']    = [{'vertices': [k_i[u], k_i[v]]} for u, v in D.edges()]
            data['faces']    = []

            if D.attributes['name'] == 'Mesh':

                for fkey in D.faces():
                    face = [k_i[k] for k in D.face[fkey]]
                    data['faces'].append({'vertices': face})

        self.camera_position = [10, -1, 10]
        self.camera_target   = [0, 0, 0]
        self.show_axes       = True
        self.vertex_size     = 20.0
        self.vertex_scale    = 0.001
        self.edge_width      = 20.0
        self.edge_scale      = 0.05

        self.data          = data
        self.height        = height
        self.width         = width
        self.sidebar_width = sidebar
        self.keycallbacks  = {}

        self.checkboxes = {}
        self.labels     = {}
        self.listboxes  = {}
        self.sliders    = {}


    # ==============================================================================
    # Setup
    # ==============================================================================

    def setup(self):

        self.main = MainWindow(application=self)
        self.main.show()

        self.setup_statusbar()
        self.setup_menubar()
        self.setup_sidebar()
        self.draw()


    # ==============================================================================
    # Start
    # ==============================================================================

    def start(self):

        sys.exit(self.exec_())


    # ==============================================================================
    # Keypress
    # ==============================================================================

    def keypress(self, obj, event):

        key = obj.GetKeySym()

        try:
            func = self.keycallbacks[key]
            func(self)
        except:
            pass


    # ==============================================================================
    # Draw
    # ==============================================================================

    def draw(self):

        self.vertices  = vtkPoints()
        self.polydata  = vtkPolyData()
        self.vcolors   = self.data.get('vertex_colors', None)
        self.colors    = vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)

        # Vertices

        if self.data.get('vertices', None):

            for vertex in self.data['vertices']:
                self.vertices.InsertNextPoint(vertex)

            self.polydata.SetPoints(self.vertices)
            self.draw_vertices()

        # Edges

        if self.data.get('edges', None):
            self.draw_edges()

        # Faces

        if self.data.get('faces', None):
            self.draw_faces()

        # Voxels

        if self.data.get('voxels', None) is not None:
            self.draw_voxels()

        # PolyData

        self.polydata.GetCellData().SetScalars(self.colors)

        # Vertex Colors

        if self.vcolors:

            self.vertex_colors = vtkUnsignedCharArray()
            self.vertex_colors.SetNumberOfComponents(3)

            for key in range(len(self.data['vertices'])):
                self.vertex_colors.InsertNextTypedTuple(self.vcolors.get(key, [200, 200, 200]))

            self.polydata.GetPointData().SetScalars(self.vertex_colors)

        # Axes

        self.draw_axes()

        if not self.show_axes:
            self.axes.VisibilityOff()

        # PolyData

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(self.polydata)

        self.polyactor = actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(self.edge_width * self.edge_scale)
        actor.GetProperty().SetEdgeColor([0, 0.5, 0])
        actor.GetProperty().SetInterpolationToGouraud()
        self.main.renderer.AddActor(actor)


    # ==============================================================================
    # Statusbar
    # ==============================================================================

    def setup_statusbar(self):

        self.statusbar = self.main.statusBar()
        self.main.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Status bar')


    def update_statusbar(self, text):

        self.statusbar.showMessage(text)


    # ==============================================================================
    # Menubar
    # ==============================================================================

    def setup_menubar(self):

        self.menubar = self.main.menuBar()
        self.main.setMenuBar(self.menubar)
        self.add_menu(name='File', items=['Open', 'Close'], actions=[self.dummy, self.dummy])


    def add_menu(self, name, items, actions):

        links = {}
        menu  = self.menubar.addMenu('&{0}'.format(name))

        for item, action in zip(items, actions):
            links[item] = menu.addAction('&{0}'.format(item))
            links[item].triggered.connect(action)


    def dummy(self):

        print('Dummy method!')


    # ==============================================================================
    # Sidebar
    # ==============================================================================

    def add_slider(self, name, value, min, max, callback, interval=10):

        self.sliders[name] = slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(interval)
        slider.setValue(value)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.valueChanged.connect(callback)
        self.layout.addWidget(slider)


    def add_label(self, name, text):

        self.labels[name] = label = QLabel(text)
        self.layout.addWidget(label)


    def add_checkbox(self, name, text, checked, callback):

        self.checkboxes[name] = checkbox = QCheckBox()
        checkbox.setText(text)
        checkbox.setChecked(checked)
        checkbox.stateChanged.connect(callback)
        self.layout.addWidget(checkbox)


    def add_listbox(self, name, items, callback):

        self.listboxes[name] = listbox = QComboBox()
        listbox.addItems(items)
        listbox.currentIndexChanged.connect(callback)
        self.layout.addWidget(listbox)


    def add_divider(self):

        self.layout.addWidget(QHLine())


    def setup_sidebar(self):

        self.sidebar = sidebar = QDockWidget()
        sidebar.setFixedWidth(self.sidebar_width)

        self.layout = layout = QVBoxLayout()
        layout.addStretch()

        widget = QWidget(sidebar)
        widget.setLayout(layout)
        sidebar.setWidget(widget)
        self.main.addDockWidget(Qt.LeftDockWidgetArea, sidebar)

        if self.data.get('vertices', None):
            self.add_label(name='vertices', text='Vertex size: {0}'.format(self.vertex_size))
            self.add_slider(name='vertices', value=self.vertex_size, min=0, max=100, callback=self.vertex_callback)

        if self.data.get('edges', None) or self.data.get('faces', None):
            self.add_label(name='edges', text='Edge width: {0}'.format(self.edge_width))
            self.add_slider(name='edges', value=self.edge_width, min=0, max=100, callback=self.edge_callback)
            self.add_label(name='opacity', text='Opacity: {0}'.format(100))
            self.add_slider(name='opacity', value=100, min=0, max=100, callback=self.opacity_callback)

        if self.data.get('voxels', None) is not None:
            self.add_label(name='gradient', text='Gradient: {0}'.format(0))
            self.add_slider(name='gradient', value=0, min=0, max=100, callback=self.gradient_callback)
        else:
            self.add_checkbox(name='axes', text='Show axes', checked=True, callback=self.axes_callback)


    # ==============================================================================
    # Vertices
    # ==============================================================================

    def draw_vertices(self):

        self.vertex = vertex = vtkSphereSource()
        vertex.SetRadius(self.vertex_size * self.vertex_scale)
        vertex.SetPhiResolution(10)
        vertex.SetThetaResolution(10)

        mapper = vtkGlyph3DMapper()
        mapper.SetInputData(self.polydata)
        mapper.SetSourceConnection(vertex.GetOutputPort())
        mapper.ScalingOff()
        mapper.ScalarVisibilityOff()

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetDiffuseColor(0.5, 0.5, 1.0)
        actor.GetProperty().LightingOff()
        actor.GetProperty().SetDiffuse(1.0)
        self.main.renderer.AddActor(actor)


    def vertex_callback(self):

        value = self.sliders['vertices'].value()
        self.labels['vertices'].setText('Vertex size: {0}'.format(value))
        self.vertex.SetRadius(value * self.vertex_scale)
        self.main.window.Render()


    def update_vertices_coordinates(self, coordinates):

        for key, xyz in coordinates.items():
            self.vertices.SetPoint(key, xyz)

        self.vertices.Modified()
        self.main.window.Render()


    def update_vertices_colors(self, colors):

        self.vertex_colors = vtkUnsignedCharArray()
        self.vertex_colors.SetNumberOfComponents(3)

        for color in [colors.get(i, [200, 200, 200]) for i in range(len(self.data['vertices']))]:
            self.vertex_colors.InsertNextTypedTuple([int(round(i)) for i in color])

        self.polydata.GetPointData().SetScalars(self.vertex_colors)
        self.main.window.Render()


    # ==============================================================================
    # Edges
    # ==============================================================================

    def draw_edges(self):

        edges = vtkCellArray()

        for edge in self.data['edges']:

            line = vtkLine()
            line.GetPointIds().SetId(0, edge['vertices'][0])
            line.GetPointIds().SetId(1, edge['vertices'][1])
            edges.InsertNextCell(line)

            color = edge.get('color', [255, 100, 100])
            try:
                self.colors.InsertNextTypedTuple(color)
            except Exception:
                self.colors.InsertNextTupleValue(color)

        self.polydata.SetLines(edges)


    def edge_callback(self):

        value = self.sliders['edges'].value()
        self.labels['edges'].setText('Edge width: {0}'.format(value))

        if value == 0:
            self.polyactor.GetProperty().EdgeVisibilityOff()
        else:
            self.polyactor.GetProperty().EdgeVisibilityOn()

        self.polyactor.GetProperty().SetLineWidth(value * self.edge_scale)
        self.main.window.Render()


    # ==============================================================================
    # Faces
    # ==============================================================================

    def draw_faces(self):

        faces = vtkCellArray()

        for face in self.data['faces']:

            vil = vtkIdList()

            for pt in face['vertices']:
                vil.InsertNextId(pt)

            faces.InsertNextCell(vil)
            color = face.get('color', [150, 255, 150])

            try:
                self.colors.InsertNextTypedTuple(color)
            except Exception:
                self.colors.InsertNextTupleValue(color)

        self.polydata.SetPolys(faces)
        self.main.window.Render()


    def opacity_callback(self):

        value = self.sliders['opacity'].value()
        self.labels['opacity'].setText('Opacity: {0}'.format(value))
        self.polyactor.GetProperty().SetOpacity(value * 0.01)

        self.main.window.Render()


    # ==============================================================================
    # Voxels
    # ==============================================================================

    def draw_voxels(self):

        self.show_axes = False

        u = self.data['voxels']
        u /= (2 * max([abs(min(u)), abs(max(u))]))
        u += 0.5
        u *= 255

        nx, ny, nz = u.shape
        dstr = asarray(u, dtype=uint8).tostring()

        img = vtkImageImport()
        img.CopyImportVoidPointer(dstr, len(dstr))
        img.SetDataScalarTypeToUnsignedChar()
        img.SetNumberOfScalarComponents(1)
        img.SetDataExtent( 0, nz - 1, 0, ny - 1, 0, nx - 1)
        img.SetWholeExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)

        self.gradient = gradient = vtkPiecewiseFunction()
        gradient.AddPoint(1, 0.0)
        gradient.AddPoint(255, 0.2)

        self.cbar = cbar = vtkColorTransferFunction()
        cbar.AddRGBPoint(  0.0, 0.0, 0.0, 1.0)
        cbar.AddRGBPoint( 42.0, 0.0, 0.5, 1.0)
        cbar.AddRGBPoint( 84.0, 0.0, 1.0, 0.5)
        cbar.AddRGBPoint(128.0, 0.0, 1.0, 0.0)
        cbar.AddRGBPoint(168.0, 0.5, 1.0, 0.0)
        cbar.AddRGBPoint(212.0, 1.0, 0.5, 0.0)
        cbar.AddRGBPoint(255.0, 1.0, 0.0, 0.0)

        self.volprop = volprop = vtkVolumeProperty()
        volprop.SetColor(cbar)
        volprop.SetScalarOpacity(gradient)
        volprop.ShadeOff()
        volprop.SetInterpolationTypeToLinear()

        mapper = vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(img.GetOutputPort())

        volume = vtkVolume()
        volume.SetMapper(mapper)
        volume.SetProperty(volprop)
        self.main.renderer.AddVolume(volume)

        self.main.camera.SetPosition(0, -2 * max([nx, ny, nz]), nz)
        self.main.camera.SetFocalPoint(0.5 * nx, 0.5 * ny, 0.5 * nz)


    def gradient_callback(self):

        value = self.sliders['gradient'].value()
        self.labels['gradient'].setText('Gradient: {0}'.format(value))

        self.gradient = gradient = vtkPiecewiseFunction()
        gradient.AddPoint(0, 0.2)
        if value:
            gradient.AddPoint(127 - value * 1.27, 0.0)
            gradient.AddPoint(127 + value * 1.27, 0.0)
        else:
            gradient.AddPoint(128, 0.2)
        gradient.AddPoint(255, 0.2)

        self.volprop.SetScalarOpacity(gradient)
        self.main.window.Render()


    # ==============================================================================
    # Axes
    # ==============================================================================

    def draw_axes(self):

        self.axes = axes = vtkAxesActor()
        axes.AxisLabelsOff()
        axes.SetConeRadius(0.2)
        self.main.renderer.AddActor(axes)


    def axes_callback(self):

        if self.checkboxes['axes'].isChecked():
            self.axes.VisibilityOn()
        else:
            self.axes.VisibilityOff()

        self.main.window.Render()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==============================================================================
    # Mesh
    # ==============================================================================

    # def func(self):
    #     self.update_vertices_colors(colors={0: [255, 0, 0], 1: [0, 255, 0], 5: [0, 0, 255]})
    #     print('Colour change!')

    # data = {
    #     'vertices': [
    #         [-3, -3, 0],
    #         [+3, -3, 0],
    #         [+3, +3, 0],
    #         [-3, +3, 0],
    #         [-3, -3, 3],
    #         [+3, -3, 3],
    #         [+3, +3, 3],
    #         [-3, +3, 3],
    #     ],
    #     # turn on vertex coloring by uncommenting
    #     # 'vertex_colors': {
    #     #     0: [255, 0, 255],
    #     #     1: [255, 0, 0],
    #     #     2: [255, 255, 0],
    #     #     3: [255, 255, 0],
    #     #     4: [0, 255, 0],
    #     #     5: [0, 255, 150],
    #     #     6: [0, 255, 255],
    #     #     7: [0, 0, 255],
    #     # },
    #     'edges': [
    #         {'vertices': [0, 4], 'color': [0, 0, 0]},
    #         {'vertices': [1, 5], 'color': [0, 0, 255]},
    #         {'vertices': [2, 6], 'color': [0, 255, 0]},
    #         {'vertices': [3, 7]}
    #     ],
    #     'faces': [
    #         {'vertices': [4, 5, 6], 'color': [250, 150, 150]},
    #         {'vertices': [6, 7, 4], 'color': [150, 150, 250]},
    #     ],
    # }

    # viewer = VtkViewer(data=data)
    # viewer.keycallbacks['s'] = func
    # viewer.setup()
    # viewer.update_vertices_coordinates(coordinates={0: [-3, -3, -2], 3: [-3, +3, -2]})
    # viewer.start()


    # ==============================================================================
    # Voxels
    # ==============================================================================

    # from numpy import linspace
    # from numpy import meshgrid

    # r       = linspace(-1, 1, 50)
    # x, y, z = meshgrid(r, r, r)

    # data = {'voxels': x + y + z}

    # viewer = VtkViewer(data=data)
    # viewer.setup()
    # viewer.start()


    # ==============================================================================
    # Datastructure
    # ==============================================================================

    from compas.datastructures import Mesh

    import compas

    datastructure = Mesh.from_obj(compas.get('quadmesh.obj'))

    viewer = VtkViewer(datastructure=datastructure)
    viewer.setup()
    viewer.start()
