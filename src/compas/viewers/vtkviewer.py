
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from vtk import vtkActor
    from vtk import vtkAxesActor
    from vtk import vtkCellArray
    from vtk import vtkCamera
    from vtk import vtkCubeSource
    from vtk import vtkGlyph3DMapper
    from vtk import vtkIdList
    from vtk import vtkInteractorStyleTrackballCamera
    from vtk import vtkLine
    from vtk import vtkPolyData
    from vtk import vtkPolyDataMapper
    from vtk import vtkPoints
    from vtk import vtkRenderer
    from vtk import vtkRenderWindow
    from vtk import vtkRenderWindowInteractor
    from vtk import vtkSliderRepresentation2D
    from vtk import vtkSliderWidget
    from vtk import vtkSphereSource
    from vtk import vtkUnsignedCharArray
    import vtk

except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VtkViewer',
]


class VtkViewer(object):

    def __init__(self, name='VTK Viewer', width=1000, height=700, data={}):

        # Note: vertex indices currently need to be given as a series of keys starting from 0.

        self.settings = {
            'draw_axes'     : True,
            'draw_vertices' : True,
            'draw_edges'    : True,
            'draw_faces'    : True,
            'draw_blocks'   : True,
            'vertex_size'   : 0.05,
            'edge_width'    : 2,
            'camera_pos'    : [10, -1, 10],
            'camera_focus'  : [0, 0, 0],
            'camera_azi'    : 30,
            'camera_ele'    : 0,
        }
        self.keycallbacks = {}
        self.data = data
        self.name = name
        self.height = height
        self.width = width
        self.setup(width=self.width, height=self.height, name=self.name)

    def keypress(self, obj, event):

        key = obj.GetKeySym()
        try:
            func = self.keycallbacks[key]
            func(self)
        except Exception:
            print('No callback for keypress {0}'.format(key))

    def camera(self):

        x, y, z = self.settings['camera_pos']
        u, v, w = self.settings['camera_focus']

        self.camera = camera = vtkCamera()
        camera.SetViewUp(0, 0, 1)
        camera.SetPosition(x, y, z)
        camera.SetFocalPoint(u, v, w)
        camera.Azimuth(self.settings['camera_azi'])
        camera.Elevation(self.settings['camera_ele'])

    def setup(self, width, height, name):

        self.camera()

        self.renderer = renderer = vtkRenderer()
        renderer.SetBackground(1.0, 1.0, 1.0)
        renderer.SetBackground2(0.8, 0.8, 0.8)
        renderer.GradientBackgroundOn()
        renderer.SetActiveCamera(self.camera)
        renderer.ResetCamera()
        renderer.ResetCameraClippingRange()

        self.window = window = vtkRenderWindow()
        window.SetSize(width, height)
        window.SetWindowName(name)
        window.AddRenderer(renderer)

        self.interactor = interactor = vtkRenderWindowInteractor()
        interactor.SetInteractorStyle(InteractorStyle())
        interactor.SetRenderWindow(window)
        interactor.AddObserver('KeyPressEvent', self.keypress)

    def draw_axes(self):

        axes = vtkAxesActor()
        axes.AxisLabelsOff()
        self.renderer.AddActor(axes)

    def draw_vertices(self):

        self.vertex = vertex = vtkSphereSource()
        vertex.SetRadius(self.settings['vertex_size'])
        vertex.SetPhiResolution(15)
        vertex.SetThetaResolution(15)

        m1 = vtkGlyph3DMapper()
        m1.SetInputData(self.poly)
        m1.SetSourceConnection(vertex.GetOutputPort())
        m1.ScalingOff()
        m1.ScalarVisibilityOff()

        a1 = vtkActor()
        a1.SetMapper(m1)
        a1.GetProperty().SetDiffuseColor(0.4, 0.4, 1.0)
        a1.GetProperty().SetDiffuse(.8)
        self.renderer.AddActor(a1)

        if self.data.get('fixed', None):

            self.support = support = vtkSphereSource()
            support.SetRadius(self.settings['vertex_size'] * 1.5)
            support.SetPhiResolution(15)
            support.SetThetaResolution(15)

            m2 = vtkGlyph3DMapper()
            m2.SetInputData(self.bcs)
            m2.SetSourceConnection(support.GetOutputPort())
            m2.ScalingOff()
            m2.ScalarVisibilityOff()

            a2 = vtkActor()
            a2.SetMapper(m2)
            a2.GetProperty().SetDiffuseColor(1.0, 0.5, 0.0)
            a2.GetProperty().SetDiffuse(.8)
            self.renderer.AddActor(a2)

        else:
            self.support = None

    def draw_edges(self):

        if self.data.get('edges', None):
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
            self.poly.SetLines(edges)

    def draw_faces(self):

        if self.data.get('faces', None):
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
            self.poly.SetPolys(faces)

    def draw_blocks(self):

        if self.data.get('blocks', None):
            size = self.data['blocks'].get('size', None)
            locations = self.data['blocks'].get('locations', None)
            for xyz in locations:
                self.locations.InsertNextPoint(xyz)
            self.blocks.SetPoints(self.locations)

            self.block = block = vtkCubeSource()
            block.SetXLength(size)
            block.SetYLength(size)
            block.SetZLength(size)

            mapper = vtkGlyph3DMapper()
            mapper.SetInputData(self.blocks)
            mapper.SetSourceConnection(block.GetOutputPort())

            self.block_actor = actor = vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetDiffuseColor(0.7, 0.7, 1.0)
            actor.GetProperty().SetDiffuse(.8)
            actor.GetProperty().EdgeVisibilityOn()
            self.renderer.AddActor(actor)
        else:
            self.block_actor = None

    def draw(self):

        self.poly = vtkPolyData()
        self.blocks = vtkPolyData()
        self.bcs = vtkPolyData()
        self.vertices = vtkPoints()
        self.locations = vtkPoints()
        self.bc_pts = vtkPoints()
        self.colors = vtkUnsignedCharArray()
        self.colors.SetNumberOfComponents(3)
        self.vcolors = self.data.get('vcolors', None)

        if self.data.get('vertices', None):
            for key, vertex in self.data['vertices'].items():
                self.vertices.InsertNextPoint(vertex)
            self.poly.SetPoints(self.vertices)

        if self.data.get('fixed', None):
            for key in self.data['fixed']:
                self.bc_pts.InsertNextPoint(self.data['vertices'][key])
            self.bcs.SetPoints(self.bc_pts)

        if self.settings['draw_axes']:
            self.draw_axes()

        if self.settings['draw_vertices']:
            self.draw_vertices()

        if self.settings['draw_edges']:
            self.draw_edges()

        if self.settings['draw_faces']:
            self.draw_faces()

        if self.settings['draw_blocks']:
            self.draw_blocks()

        # Actor

        self.poly.GetCellData().SetScalars(self.colors)
        if self.vcolors:
            self.vertex_colors = vtkUnsignedCharArray()
            self.vertex_colors.SetNumberOfComponents(3)
            for key in self.data['vertices']:
                self.vertex_colors.InsertNextTypedTuple(self.vcolors.get(key, [200, 200, 200]))
            self.poly.GetPointData().SetScalars(self.vertex_colors)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(self.poly)

        self.actor = actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(self.settings['edge_width'])
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetEdgeColor([0, 0.5, 0])
        actor.GetProperty().SetOpacity(1.0)
        actor.GetProperty().SetInterpolationToGouraud()
        self.renderer.AddActor(actor)

    def gui(self):

        w = 0.005
        h = 0.015
        l = 0.015
        y = 0.90
        a = 0.01
        b = 0.10

        vertex_size = self.settings['vertex_size']
        edge_width  = self.settings['edge_width']

        if self.settings['draw_vertices']:
            self.slider_vertex = self.slider(w, h, l, [a, y], [b, y], 0.0, 0.2, vertex_size, 'Vertex size')
            self.slider_vertex.AddObserver(vtk.vtkCommand.InteractionEvent, VertexSizeCallback(self.vertex, self.support))
            y -= 0.12

        if self.settings['draw_edges']:
            self.slider_edge = self.slider(w, h, l, [a, y], [b, y], 0.01, 20.0, edge_width, 'Edge width')
            self.slider_edge.AddObserver(vtk.vtkCommand.InteractionEvent, EdgeWidthCallback(self.actor))
            y -= 0.12

        self.slider_opacity = self.slider(w, h, l, [a, y], [b, y], 0.0, 1.0, 1.0, 'Opacity')
        self.slider_opacity.AddObserver(vtk.vtkCommand.InteractionEvent, OpacityCallback(self.actor, self.block_actor))
        y -= 0.12

    def start(self):

        self.draw()
        self.gui()
        self.interactor.Initialize()
        self.window.Render()
        self.interactor.Start()

    def slider(self, width, height, label, posy, posx, minimum, maximum, value, text):

        slider = vtkSliderRepresentation2D()
        slider.SetMinimumValue(minimum)
        slider.SetMaximumValue(maximum)
        slider.SetValue(value)
        slider.SetTitleText(text)
        slider.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
        slider.GetPoint1Coordinate().SetValue(posy[0], posy[1])
        slider.GetPoint2Coordinate().SetValue(posx[0], posx[1])
        slider.SetTubeWidth(width)
        slider.SetTitleHeight(height)
        slider.SetLabelHeight(label)

        sliderwidget = vtkSliderWidget()
        sliderwidget.SetInteractor(self.interactor)
        sliderwidget.SetRepresentation(slider)
        sliderwidget.SetAnimationModeToAnimate()
        sliderwidget.EnabledOn()

        return sliderwidget


class InteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver('LeftButtonPressEvent', self.LeftButtonPressEvent)
        self.AddObserver('LeftButtonReleaseEvent', self.LeftButtonReleaseEvent)
        self.AddObserver('MiddleButtonPressEvent', self.MiddleButtonPressEvent)
        self.AddObserver('MiddleButtonReleaseEvent', self.MiddleButtonReleaseEvent)
        self.AddObserver('RightButtonPressEvent', self.RightButtonPressEvent)
        self.AddObserver('RightButtonReleaseEvent', self.RightButtonReleaseEvent)

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


class VertexSizeCallback(object):

    def __init__(self, vertex, support):
        self.vertex = vertex
        self.support = support

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        self.vertex.SetRadius(value)
        if self.support:
            self.support.SetRadius(value * 1.5)


class EdgeWidthCallback(object):

    def __init__(self, actor):
        self.actor = actor

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        self.actor.GetProperty().SetLineWidth(value)


class OpacityCallback(object):

    def __init__(self, actor, block_actor):
        self.actor = actor
        self.block_actor = block_actor

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        self.actor.GetProperty().SetOpacity(value)
        self.block_actor.GetProperty().SetOpacity(value)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    def func(self):
        print('Callback')


    data = {
        'vertices': {
            0: [-3, -3, 0],
            1: [+3, -3, 0],
            2: [+3, +3, 0],
            3: [-3, +3, 0],
            4: [-3, -3, 2],
            5: [+3, -3, 2],
            6: [+3, +3, 2],
            7: [-3, +3, 2],
        },
        'vcolors': {  # turn on vertex coloring by uncommenting below
            # 0: [255, 0, 255],
            # 1: [255, 0, 0],
            # 2: [255, 255, 0],
            # 3: [255, 255, 0],
            # 4: [0, 255, 0],
            # 5: [0, 255, 150],
            # 6: [0, 255, 255],
            # 7: [0, 0, 255],
        },
        'edges': [
            {'u': 0, 'v': 4, 'color': [0, 0, 0]},
            {'u': 1, 'v': 5, 'color': [0, 0, 255]},
            {'u': 2, 'v': 6, 'color': [0, 255, 0]},
            {'u': 3, 'v': 7}
        ],
        'faces': {
            0: {'vertices': [4, 5, 6], 'color': [250, 150, 150]},
            1: {'vertices': [6, 7, 4], 'color': [150, 150, 250]},
        },
        'fixed': [0, 1],
        'blocks': {
            'size': 1,
            'locations': [[0, 0, 3], [0, 0, 4]],
        }
    }

    viewer = VtkViewer(data=data)
    viewer.settings['draw_axes'] = 1
    viewer.settings['draw_vertices'] = 1
    viewer.settings['draw_edges'] = 1
    viewer.settings['draw_faces'] = 1
    viewer.settings['draw_blocks'] = 1
    viewer.keycallbacks['s'] = func
    viewer.start()
