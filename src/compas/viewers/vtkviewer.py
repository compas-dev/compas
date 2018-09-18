
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from vtk import vtkActor
    from vtk import vtkAxesActor
    from vtk import vtkCamera
    from vtk import vtkCellArray
    from vtk import vtkColorTransferFunction
    from vtk import vtkCubeSource
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

    def __init__(self, app, parent=None):
        QMainWindow.__init__(self, parent)

        # Camera

        x, y, z = app.camera_position
        u, v, w = app.camera_target

        self.camera = camera = vtkCamera()
        camera.SetViewUp(0, 0, 1)
        camera.SetPosition(x, y, z)
        camera.SetFocalPoint(u, v, w)

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

        self.frame = frame = QFrame()
        self.widget = widget = QVTKRenderWindowInteractor(frame, rw=window)
        self.layout = layout = QVBoxLayout()
        layout.addWidget(widget)

        frame.setLayout(layout)

        # Interactor

        self.interactor = interactor = widget.GetRenderWindow().GetInteractor()
        interactor.SetInteractorStyle(InteractorStyle())
        interactor.AddObserver('KeyPressEvent', app.keypress)
        interactor.Initialize()
        interactor.Start()

        self.resize(app.width, app.height)
        self.setCentralWidget(frame)


# ==============================================================================
# InteractorStyle
# ==============================================================================

class InteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):

        self.AddObserver('LeftButtonPressEvent',     self.LeftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent',   self.LeftButtonReleaseEvent)
        self.AddObserver('MiddleButtonPressEvent',   self.MiddleButtonPressEvent)
        self.AddObserver('MiddleButtonReleaseEvent', self.MiddleButtonReleaseEvent)
        self.AddObserver('RightButtonPressEvent',    self.RightButtonPressEvent)
        self.AddObserver('RightButtonReleaseEvent',  self.RightButtonReleaseEvent)

    def LeftButtonPressEvent(self, obj, event):

        self.OnLeftButtonDown()
        return

    def LeftButtonReleaseEvent(self, obj, event):

        self.OnLeftButtonUp()
        return

    def MiddleButtonPressEvent(self, obj, event):

        self.OnMiddleButtonDown()
        return

    def MiddleButtonReleaseEvent(self, obj, event):

        self.OnMiddleButtonUp()
        return

    def RightButtonPressEvent(self, obj, event):

        self.OnRightButtonDown()
        return

    def RightButtonReleaseEvent(self, obj, event):

        self.OnRightButtonUp()
        return


# ==============================================================================
# VtkViewer
# ==============================================================================

class VtkViewer(QApplication):

    def __init__(self, name='VTK Viewer', data={}, height=900, width=1440, datastructure=None):
        QApplication.__init__(self, sys.argv)

        if datastructure:

            i_k = datastructure.index_key()
            k_i = datastructure.index_key()
            data = {}

            data['vertices'] = {i: datastructure.vertex_coordinates(i_k[i])
                                for i in range(datastructure.number_of_vertices())}

            data['edges']    = [{'u': k_i[u], 'v': k_i[v]} for u, v in datastructure.edges()]

            data['fixed']    = [k_i[key] for key in datastructure.vertices()
                                if datastructure.vertex[key].get('is_fixed')]

            if datastructure.attributes['name'] == 'Mesh':
                data['faces']    = {i: {'vertices': datastructure.face[i]} for i in datastructure.faces()}

        self.camera_position = [10, -1, 10]
        self.camera_target   = [0, 0, 0]
        self.show_axes       = True
        self.vertex_size     = 20.0
        self.vertex_scale    = 0.001
        self.edge_width      = 20.0
        self.edge_scale      = 0.05

        self.name         = name
        self.data         = data
        self.height       = height
        self.width        = width
        self.keycallbacks = {}

        self.labels     = {}
        self.listboxes  = {}
        self.sliders    = {}
        self.checkboxes = {}


    # ==============================================================================
    # Setup
    # ==============================================================================

    def setup(self):

        self.main = MainWindow(app=self)
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
        self.blocks    = vtkPolyData()
        self.locations = vtkPoints()
        self.bcs       = vtkPolyData()
        self.fixed     = vtkPoints()
        self.colors    = vtkUnsignedCharArray()
        self.vcolors   = self.data.get('vertex_colors', None)
        self.colors.SetNumberOfComponents(3)

        if self.data.get('vertices', None):
            for key, vertex in self.data['vertices'].items():
                self.vertices.InsertNextPoint(vertex)
            self.polydata.SetPoints(self.vertices)
            self.draw_vertices()

        if self.data.get('fixed', None):
            for key in self.data['fixed']:
                self.fixed.InsertNextPoint(self.data['vertices'][key])
            self.bcs.SetPoints(self.fixed)

        if self.data.get('edges', None):
            self.draw_edges()

        if self.data.get('faces', None):
            self.draw_faces()

        if self.data.get('blocks', None):
            self.draw_blocks()
        else:
            self.block_actor = None

        if self.data.get('voxels', None) is not None:
            self.draw_voxels()

        self.polydata.GetCellData().SetScalars(self.colors)

        if self.vcolors:
            self.vertex_colors = vtkUnsignedCharArray()
            self.vertex_colors.SetNumberOfComponents(3)
            for key in self.data['vertices']:
                self.vertex_colors.InsertNextTypedTuple(self.vcolors.get(key, [200, 200, 200]))
            self.polydata.GetPointData().SetScalars(self.vertex_colors)

        self.draw_axes()
        if not self.show_axes:
            self.axes.VisibilityOff()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(self.polydata)

        self.actor = actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(self.edge_width * self.edge_scale)
        if self.edge_width == 0:
            actor.GetProperty().EdgeVisibilityOff()
        else:
            actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetEdgeColor([0, 0.5, 0])
        actor.GetProperty().SetInterpolationToGouraud()

        self.main.renderer.AddActor(actor)


    # ==============================================================================
    # Statusbar
    # ==============================================================================

    def setup_statusbar(self):

        self.status = self.main.statusBar()
        self.main.setStatusBar(self.status)
        self.status.showMessage('Status bar')


    def update_statusbar(self, text):

        self.status.showMessage(text)


    # ==============================================================================
    # Menus
    # ==============================================================================

    def setup_menubar(self):

        self.menu = self.main.menuBar()
        self.main.setMenuBar(self.menu)
        self.add_file_menu()
        self.add_view_menu()

    def add_file_menu(self):

        file_menu = self.menu.addMenu('&File')
        open_action = file_menu.addAction('&Open')
        open_action.triggered.connect(self.file_open)

    def add_view_menu(self):

        view_menu = self.menu.addMenu('&View')

    def file_open(self):

        print('FILE')


    # ==============================================================================
    # Sidebar
    # ==============================================================================

    def add_slider(self, name, value, minimum, maximum, interval, callback):

        self.sliders[name] = slider = QSlider(Qt.Horizontal)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(interval)
        slider.setValue(value)
        slider.setMinimum(minimum)
        slider.setMaximum(maximum)
        slider.valueChanged.connect(callback)
        self.layout.addWidget(slider)

    def add_label(self, name, text):

        self.labels[name] = label = QLabel()
        label.setText(text)
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

    def add_splitter(self):

        pass
        # self.layout.setFrameShape(QFrame.HLine)

    def setup_sidebar(self):

        self.sidebar = sidebar = QDockWidget()
        sidebar.setFixedWidth(120)

        self.layout = layout = QVBoxLayout()
        layout.addStretch()

        if self.data.get('vertices', None):

            self.add_label(name='label_vertices', text='Vertex size: {0}'.format(self.vertex_size))
            self.add_slider(name='slider_vertices', value=self.vertex_size, minimum=0, maximum=100,
                            interval=10, callback=self.vertex_callback)

        if self.data.get('edges', None) or self.data.get('faces', None):

            self.add_label(name='label_edges', text='Edge width: {0}'.format(self.edge_width))
            self.add_slider(name='slider_edges', value=self.edge_width, minimum=0, maximum=100,
                            interval=10, callback=self.edge_callback)

            self.add_label(name='label_opacity', text='Opacity: {0}'.format(100))
            self.add_slider(name='slider_opacity', value=100, minimum=0, maximum=100,
                            interval=10, callback=self.opacity_callback)

        if self.data.get('voxels', None) is not None:

            self.add_label(name='label_gradient', text='Gradient: {0}'.format(0))
            self.add_slider(name='slider_gradient', value=0, minimum=0, maximum=100,
                            interval=10, callback=self.gradient_callback)

        widget = QWidget(self.sidebar)
        widget.setLayout(layout)

        self.sidebar.setWidget(widget)
        self.main.addDockWidget(Qt.LeftDockWidgetArea, sidebar)


    # ==============================================================================
    # Vertices
    # ==============================================================================

    def draw_vertices(self):

        self.vertex = vertex = vtkSphereSource()
        vertex.SetRadius(self.vertex_size * self.vertex_scale)
        vertex.SetPhiResolution(15)
        vertex.SetThetaResolution(15)

        mapper1 = vtkGlyph3DMapper()
        mapper1.SetInputData(self.polydata)
        mapper1.SetSourceConnection(vertex.GetOutputPort())
        mapper1.ScalingOff()
        mapper1.ScalarVisibilityOff()

        actor1 = vtkActor()
        actor1.SetMapper(mapper1)
        actor1.GetProperty().SetDiffuseColor(0.6, 0.6, 1.0)
        actor1.GetProperty().SetDiffuse(1.0)
        self.main.renderer.AddActor(actor1)

        if self.data.get('fixed', None):

            self.support = support = vtkSphereSource()
            support.SetRadius(self.vertex_size * 1.5 * self.vertex_scale)
            support.SetPhiResolution(15)
            support.SetThetaResolution(15)

            mapper2 = vtkGlyph3DMapper()
            mapper2.SetInputData(self.bcs)
            mapper2.SetSourceConnection(support.GetOutputPort())
            mapper2.ScalingOff()
            mapper2.ScalarVisibilityOff()

            actor2 = vtkActor()
            actor2.SetMapper(mapper2)
            actor2.GetProperty().SetDiffuseColor(1.0, 0.8, 0.0)
            actor2.GetProperty().SetDiffuse(1.0)
            self.main.renderer.AddActor(actor2)

        else:
            self.support = None

    def vertex_callback(self):

        value = self.sliders['slider_vertices'].value()
        self.labels['label_vertices'].setText('Vertex size: {0}'.format(value))
        self.vertex.SetRadius(value * self.vertex_scale)
        if self.support:
            self.support.SetRadius(value * 1.5 * self.vertex_scale)
        self.main.window.Render()

    def update_vertices_coordinates(self, coordinates):

        for key, xyz in coordinates.items():
            self.vertices.SetPoint(key, xyz)
        self.vertices.Modified()
        self.main.window.Render()

    def update_vertices_colors(self, colors):

        self.vertex_colors = vtkUnsignedCharArray()
        self.vertex_colors.SetNumberOfComponents(3)
        colors_ = [colors.get(i, [200, 200, 200]) for i in self.data['vertices'].keys()]
        for color in colors_:
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
            line.GetPointIds().SetId(0, edge['u'])
            line.GetPointIds().SetId(1, edge['v'])
            edges.InsertNextCell(line)
            color = edge.get('color', [255, 100, 100])

            try:
                self.colors.InsertNextTypedTuple(color)
            except Exception:
                self.colors.InsertNextTupleValue(color)

        self.polydata.SetLines(edges)

    def edge_callback(self):

        value = self.sliders['slider_edges'].value()
        if value == 0:
            self.actor.GetProperty().EdgeVisibilityOff()
        else:
            self.actor.GetProperty().EdgeVisibilityOn()
        self.labels['label_edges'].setText('Edge width: {0}'.format(value))
        self.actor.GetProperty().SetLineWidth(value * self.edge_scale)
        self.main.window.Render()


    # ==============================================================================
    # Faces
    # ==============================================================================

    def draw_faces(self):

        faces = vtkCellArray()

        for fkey, face in self.data['faces'].items():

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

    def opacity_callback(self):

        value = self.sliders['slider_opacity'].value()
        self.labels['label_opacity'].setText('Opacity: {0}'.format(value))
        self.actor.GetProperty().SetOpacity(value * 0.01)
        if self.block_actor:
            self.block_actor.GetProperty().SetOpacity(value * 0.01)
        self.main.window.Render()


    # ==============================================================================
    # Blocks
    # ==============================================================================

    def draw_blocks(self):

        for location in self.data['blocks'].get('locations', []):
            self.locations.InsertNextPoint(location)
        self.blocks.SetPoints(self.locations)

        self.block = block = vtkCubeSource()
        size = self.data['blocks'].get('size', 1)
        block.SetXLength(size)
        block.SetYLength(size)
        block.SetZLength(size)

        mapper = vtkGlyph3DMapper()
        mapper.SetInputData(self.blocks)
        mapper.SetSourceConnection(block.GetOutputPort())

        self.block_actor = actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetDiffuseColor(0.7, 0.7, 1.0)
        actor.GetProperty().SetDiffuse(1.0)
        actor.GetProperty().EdgeVisibilityOn()
        self.main.renderer.AddActor(actor)


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
        U = asarray(u, dtype=uint8)
        dstr = U.tostring()

        img = vtkImageImport()
        img.CopyImportVoidPointer(dstr, len(dstr))
        img.SetDataScalarTypeToUnsignedChar()
        img.SetNumberOfScalarComponents(1)
        img.SetDataExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)
        img.SetWholeExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)

        self.gradient = gradient = vtkPiecewiseFunction()
        gradient.AddPoint(1, 0.0)
        gradient.AddPoint(255, 0.2)

        self.cbar = cbar = vtkColorTransferFunction()
        cbar.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
        cbar.AddRGBPoint(42.0, 0.0, 0.5, 1.0)
        cbar.AddRGBPoint(84.0, 0.0, 1.0, 0.5)
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

        value = self.sliders['slider_gradient'].value()
        self.labels['label_gradient'].setText('Gradient: {0}'.format(value))

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
    # Axis
    # ==============================================================================

    def draw_axes(self):

        self.axes = axes = vtkAxesActor()
        axes.AxisLabelsOff()
        axes.SetConeRadius(0.2)
        self.main.renderer.AddActor(axes)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # ==============================================================================
    # Mesh
    # ==============================================================================

    # def func(self):
    #     print('Callback test!')

    # data = {
    #     'vertices': {
    #         0: [-3, -3, 0],
    #         1: [+3, -3, 0],
    #         2: [+3, +3, 0],
    #         3: [-3, +3, 0],
    #         4: [-3, -3, 3],
    #         5: [+3, -3, 3],
    #         6: [+3, +3, 3],
    #         7: [-3, +3, 3],
    #     },
    #     'vertex_colors': {
    #         # turn on vertex coloring by uncommenting
    #         0: [255, 0, 255],
    #         1: [255, 0, 0],
    #         2: [255, 255, 0],
    #         3: [255, 255, 0],
    #         4: [0, 255, 0],
    #         5: [0, 255, 150],
    #         6: [0, 255, 255],
    #         7: [0, 0, 255],
    #     },
    #     'edges': [
    #         {'u': 0, 'v': 4, 'color': [0, 0, 0]},
    #         {'u': 1, 'v': 5, 'color': [0, 0, 255]},
    #         {'u': 2, 'v': 6, 'color': [0, 255, 0]},
    #         {'u': 3, 'v': 7}
    #     ],
    #     'faces': {
    #         0: {'vertices': [4, 5, 6], 'color': [250, 150, 150]},
    #         1: {'vertices': [6, 7, 4], 'color': [150, 150, 250]},
    #     },
    #     'fixed':
    #         [0, 1],
    #     'blocks': {
    #         'size': 1,
    #         'locations': [[0, 0, 3], [0, 0, 4]],
    #     }
    # }

    # viewer = VtkViewer(data=data)
    # viewer.show_axes = False
    # viewer.keycallbacks['s'] = func
    # viewer.setup()
    # viewer.start()


    # ==============================================================================
    # Voxels
    # ==============================================================================

    # from numpy import linspace
    # from numpy import meshgrid

    # r = linspace(-1, 1, 50)
    # x, y, z = meshgrid(r, r, r)

    # data = {
    #     'voxels': x + y + z,
    # }

    # viewer = VtkViewer(data=data)
    # viewer.setup()
    # viewer.start()


    # ==============================================================================
    # Datastructures
    # ==============================================================================

    from compas.datastructures import Network
    from compas.datastructures import Mesh

    import compas

    # datastructure = Network.from_obj(compas.get('saddle.obj'))
    datastructure = Mesh.from_obj(compas.get('quadmesh.obj'))

    viewer = VtkViewer(datastructure=datastructure)
    viewer.setup()
    viewer.start()
