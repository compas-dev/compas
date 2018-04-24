
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from vtk import vtkAxesActor
    from vtk import vtkCamera
    from vtk import vtkColorTransferFunction
    from vtk import vtkFixedPointVolumeRayCastMapper
    from vtk import vtkImageImport
    from vtk import vtkInteractorStyleTrackballCamera
    from vtk import vtkPiecewiseFunction
    from vtk import vtkRenderer
    from vtk import vtkRenderWindow
    from vtk import vtkRenderWindowInteractor
    from vtk import vtkSliderRepresentation2D
    from vtk import vtkSliderWidget
    from vtk import vtkVolume
    from vtk import vtkVolumeProperty
    import vtk
except ImportError:
    pass

try:
    from numpy import asarray
    from numpy import max
    from numpy import uint8
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'VtkVoxels',
]


class VtkVoxels(object):

    def __init__(self, data, name='VTK Voxels', width=1000, height=700):

        self.keycallbacks = {}
        self.data = data
        self.size = data.shape
        self.name = name
        self.height = height
        self.width = width
        self.setup(width=self.width, height=self.height, name=self.name)

    def keypress(self, obj, event):

        key = obj.GetKeySym()
        try:
            func = self.keycallbacks[key]
            func(self)
        except:
            print('No callback for keypress {0}'.format(key))

    def draw_axes(self):

        axes = vtkAxesActor()
        axes.AxisLabelsOff()
        self.renderer.AddActor(axes)

    def camera(self):

        a, b, c = self.size
        x, y, z = [0.1 * a, -3 * b, c]
        u, v, w = [0.5 * a, 0.5 * b, 0.5 * c]

        self.camera = camera = vtkCamera()
        camera.SetViewUp(0, 0, 1)
        camera.SetPosition(x, y, z)
        camera.SetFocalPoint(u, v, w)

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

    def draw(self):

        self.draw_axes()

        u = self.data
        u /= max(u)
        u *= 255
        nx, ny, nz = self.size
        U = asarray(u, dtype=uint8)

        img = vtkImageImport()
        dstr = U.tostring()
        img.CopyImportVoidPointer(dstr, len(dstr))
        img.SetDataScalarTypeToUnsignedChar()
        img.SetNumberOfScalarComponents(1)
        img.SetDataExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)
        img.SetWholeExtent(0, nz - 1, 0, ny - 1, 0, nx - 1)

        self.opacity = opacity = vtkPiecewiseFunction()
        opacity.AddPoint(0, 0.0)
        opacity.AddPoint(255, 0.2)

        self.cbar = cbar = vtkColorTransferFunction()
        cbar.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
        cbar.AddRGBPoint(50.0, 0.0, 0.0, 1.0)
        cbar.AddRGBPoint(100.0, 0.0, 1.0, 1.0)
        cbar.AddRGBPoint(150.0, 0.0, 1.0, 0.0)
        cbar.AddRGBPoint(200.0, 1.0, 1.0, 0.0)
        cbar.AddRGBPoint(255.0, 1.0, 0.0, 0.0)

        self.volprop = volprop = vtkVolumeProperty()
        volprop.SetColor(cbar)
        volprop.SetScalarOpacity(opacity)
        volprop.ShadeOff()
        volprop.SetInterpolationTypeToLinear()

        mapper = vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(img.GetOutputPort())
        volume = vtkVolume()
        volume.SetMapper(mapper)
        volume.SetProperty(volprop)
        self.renderer.AddVolume(volume)

    def gui(self):

        w = 0.005
        h = 0.015
        l = 0.015
        y = 0.90
        a = 0.01
        b = 0.10

        self.slider_opacity = self.slider(w, h, l, [a, y], [b, y], 0.0, 254, 0, 'Opacity')
        self.slider_opacity.AddObserver(vtk.vtkCommand.InteractionEvent, OpacityCallback(self.opacity, self.volprop))
        y -= 0.12

        self.slider_shader = self.slider(w, h, l, [a, y], [b, y], 0.0, 1, 0, 'Shader')
        self.slider_shader.AddObserver(vtk.vtkCommand.InteractionEvent, ShaderCallback(self.volprop))
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


class OpacityCallback():

    def __init__(self, opacity, volprop):
        self.opacity = opacity
        self.volprop = volprop

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        self.opacity = opacity = vtkPiecewiseFunction()
        opacity.AddPoint(value, 0.0)
        opacity.AddPoint(255, 0.2)
        self.volprop.SetScalarOpacity(opacity)


class ShaderCallback():

    def __init__(self, volprop):
        self.volprop = volprop

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        if value >= 0.5:
            self.volprop.ShadeOn()
        else:
            self.volprop.ShadeOff()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy import linspace
    from numpy import meshgrid

    r = linspace(0, 10, 50)
    x, y, z = meshgrid(r, r, r)
    data = x + y + z

    voxels = VtkVoxels(data=data)
    voxels.start()
