from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

from compas.viewers.core.helpers import Camera
from compas.viewers.core.helpers import Mouse
from compas.viewers.core.helpers import Grid
from compas.viewers.core.helpers import Axes


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Shajay Bhooshan <>']
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Viewer']


class Viewer(object):
    """Base class for defining viewers.

    Parameters
    ----------
    title : str
        The title of the viewer window. Defaults to `Viewer`.
    width : int
        The width of the viewer window. Defaults to `800`.
    height : int
        The height of the viewer window. Defaults to `600`.

    Attributes
    ----------
    title : str
        The title of the viewer window.
    width : int
        The width of the viewer window.
    height : int
        The height of the viewer window.
    near : float
        Distance of the near clipping plane. Default is `0.1`.
    far : float
        Distance of the far clipping plane. Default is `1000.0`.
    fov : float
        Field of view. Default is `50.0`.
    clear_color : 4-tuple of float
        A sequence of 4 floats defining the background color of the scene.
        Default is `(0.9, 0.9, 0.9, 1.0)`.
    grid_on : bool
        Grid on or off.
    axes_on : bool
        Grid on or off.
    mouse : Mouse
        A ``Mouse`` object.
    camera : Camera
        A ``Camera`` object.
    grid : Grid
        A ``Grid`` object.
    displayfuncs : list of callable
        A list of functions called by the display callback to render the scene.

    Notes
    -----
    Extend this class to make a custom viewer. The class has a `setup` function
    that creates a basic window and registers callback for the most common GLUT
    functions:

        * `glutDisplayFunc`
        * `glutReshapeFunc`
        * `glutTimerFunc`
        * `glutKeyboardFunc`
        * `glutMouseFunc`
        * `glutMotionFunc`
        * `glutIdleFunc`

    The callbacks are registered using a two-step mechanism. The registration is
    handled by a method `name_callback` and the implementation by a method
    `name`.

    For example: `display_callback` is registered with `glutDisplayFunc`, and
    `display_callback` calls `display` for the actual implementation. To modify
    the behaviour of the `display callback`, you should thus redefine `display`.

    Examples
    --------
    >>> viewer = Viewer(width=1440, height=900)
    >>> viewer.title = 'Big window'
    >>> viewer.setup()
    >>> viewer.show()

    """
    def __init__(self, title='Viewer', width=800, height=600, displayfuncs=None, delay_setup=True, **kwargs):
        self._mod         = 0
        self._timeout     = 10
        self._v           = 0
        self._debug       = False
        self.title        = title
        self.width        = width
        self.height       = height
        self.near         = 0.1
        self.far          = 1000.0
        self.fov          = 50.0
        self.clear_color  = (0.90, 0.90, 0.90, 1.)
        self.grid_on      = kwargs.get('grid_on', True)
        self.axes_on      = kwargs.get('axes_on', True)
        self.mouse        = Mouse(self)
        self.camera       = Camera(self)
        self.grid         = Grid()
        self.axes         = Axes()
        self.displayfuncs = displayfuncs or []
        if not delay_setup:
            self.setup()

    def setup(self):
        """Setup the viewer with the provided parameters."""
        # the viewer window
        glutInit()
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(int((glutGet(GLUT_SCREEN_WIDTH) - self.width) * 0.5),
                               int((glutGet(GLUT_SCREEN_HEIGHT) - self.height) * 0.5))
        glutCreateWindow(str.encode(self.title))
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glClearColor(*self.clear_color)
        # callback registration
        glutDisplayFunc(self._display_callback)
        glutReshapeFunc(self._reshape_callback)
        glutTimerFunc(0, self._timer_callback, 0)
        glutKeyboardFunc(self._keypress_callback)
        glutMouseFunc(self._mouseclick_callback)
        glutMotionFunc(self._mousemotion_callback)
        glutPassiveMotionFunc(self._passivemousemotion_callback)
        glutIdleFunc(self._idle_callback)
        glutSpecialFunc(self._special_callback)
        # settings
        glCullFace(GL_BACK)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPolygonOffset(1.0, 1.0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_CULL_FACE)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    def show(self):
        """Show the viewer by entering the GLUT main loop."""
        glutMainLoop()

    # ==========================================================================
    # Callbacks
    # ==========================================================================

    def _reshape_callback(self, w, h):
        """The reshape callback is triggered when a window is reshaped. A
        reshape callback is also triggered immediately before a window's first
        display callback after a window is created or whenever an overlay for
        the window is established. The width and height parameters of the
        callback specify the new window size in pixels. Before the callback, the
        current window is set to the window that has been reshaped."""
        self.reshape(w, h)

    def _idle_callback(self):
        """glutIdleFunc sets the global idle callback to be func so a GLUT
        program can perform background processing tasks or continuous animation
        when window system events are not being received. If enabled, the idle
        callback is continuously called when events are not being received. The
        callback routine has no parameters. The current window and current menu
        will not be changed before the idle callback. Programs with multiple
        windows and/or menus should explicitly set the current window and/or
        current menu and not rely on its current setting."""
        self.idle()

    def _timer_callback(self, v):
        """glutTimerFunc registers the timer callback func to be triggered in at
        least msecs milliseconds. The value parameter to the timer callback will
        be the value of the value parameter to glutTimerFunc. Multiple timer
        callbacks at same or differing times may be registered simultaneously.
        The number of milliseconds is a lower bound on the time before the
        callback is generated. GLUT attempts to deliver the timer callback as
        soon as possible after the expiration of the callback's time
        interval."""
        self._timer(v)
        self.timer(v)
        glutPostRedisplay()
        # note that the value of `v` will be equal to the value of the last
        # argument of glutTimerFunc (here `0`)
        glutTimerFunc(self._timeout, self._timer_callback, self._v)

    def _display_callback(self):
        """When GLUT determines that the normal plane for the window needs to be
        redisplayed, the display callback for the window is called. Before the
        callback, the current window is set to the window needing to be
        redisplayed and (if no overlay display callback is registered) the layer
        in use is set to the normal plane. The display callback is called with
        no parameters. The entire normal plane region should be redisplayed in
        response to the callback (this includes ancillary buffers if your
        program depends on their state)."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._display()
        self.display()
        for f in self.displayfuncs:
            f()
        glutSwapBuffers()

    # ==========================================================================
    # Inout callbacks
    # ==========================================================================

    def _keypress_callback(self, key, x, y):
        """When a user types into the window, each key press generating an ASCII
        character will generate a keyboard callback. The key callback parameter
        is the generated ASCII character. The state of modifier keys such as
        Shift cannot be determined directly; their only effect will be on the
        returned ASCII data. The x and y callback parameters indicate the mouse
        location in window relative coordinates when the key was pressed. When a
        new window is created, no keyboard callback is initially registered, and
        ASCII key strokes in the window are ignored. Passing NULL to
        glutKeyboardFunc disables the generation of keyboard callbacks."""
        self._keypress(key, x, y)
        self.keypress(key, x, y)
        glutPostRedisplay()

    def _special_callback(self, key, x, y):
        """The special keyboard callback is triggered when keyboard function or
        directional keys are pressed. The key callback parameter is a GLUT_KEY_*
        constant for the special key pressed. The x and y callback parameters
        indicate the mouse in window relative coordinates when the key was
        pressed. When a new window is created, no special callback is initially
        registered and special key strokes in the window are ignored. Passing
        NULL to glutSpecialFunc disables the generation of special callbacks.
        """
        self._mod = glutGetModifiers()
        self._special(key, x, y)
        self.special(key, x, y)
        glutPostRedisplay()

    def _mouseclick_callback(self, button, state, x, y):
        """When a user presses and releases mouse buttons in the window, each
        press and each release generates a mouse callback. The button parameter
        is one of GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, or GLUT_RIGHT_BUTTON.
        For systems with only two mouse buttons, it may not be possible to
        generate GLUT_MIDDLE_BUTTON callback. For systems with a single mouse
        button, it may be possible to generate only a GLUT_LEFT_BUTTON callback.
        The state parameter is either GLUT_UP or GLUT_DOWN indicating whether
        the callback was due to a release or press respectively. The x and y
        callback parameters indicate the window relative coordinates when the
        mouse button state changed. If a GLUT_DOWN callback for a specific
        button is triggered, the program can assume a GLUT_UP callback for the
        same button will be generated (assuming the window still has a mouse
        callback registered) when the mouse button is released even if the mouse
        has moved outside the window."""
        self.mouse.x_last = x
        self.mouse.y_last = y
        if button == GLUT_LEFT_BUTTON:
            self.mouse.buttons[0] = state == GLUT_DOWN
            self.left_mouseclick(x, y)
        elif button == GLUT_MIDDLE_BUTTON:
            self.mouse.buttons[1] = state == GLUT_DOWN
            self.middle_mouseclick(x, y)
        elif button == GLUT_RIGHT_BUTTON:
            self.mouse.buttons[2] = state == GLUT_DOWN
            self.right_mouseclick(x, y)
        glutPostRedisplay()

    def _mousemotion_callback(self, x, y):
        """The motion callback for a window is called when the mouse moves
        within the window while one or more mouse buttons are pressed. The x and
        y callback parameters indicate the mouse location in window relative
        coordinates."""
        if self.mouse.buttons[0]:
            self.left_mousemotion(x, y)
        elif self.mouse.buttons[1]:
            self.middle_mousemotion(x, y)
        elif self.mouse.buttons[2]:
            self.right_mousemotion(x, y)

    def _passivemousemotion_callback(self, x, y):
        self.mousemotion(x, y)

    # ==========================================================================
    # Callback implementations
    # ==========================================================================

    def reshape(self, w, h):
        """Default implementation of the `reshape callback`. Redefine this
        method to customize what the viewer does when it is being reshaped, i.e.
        resized.

        Parameters
        ----------
        w : int
            The new width of the viewer.
        h : int
            The new height of the viewer.

        Notes
        -----
        This function is called automatically when the viewer is resized.
        The parameters `w` and `h` are automatically provided by the caller
        and correspond to the `live` size of the window. The function is
        also called when the window is initialized ,i.e. when it is given
        its initial size.

        """
        self.width = w
        self.height = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = float(w) / float(h)
        gluPerspective(self.fov, aspect, self.near, self.far)

    def idle(self):
        """Default implementation of the `idle callback`. Redefine this method
        to customise what the viewer does when it is idle.
        """
        pass

    def _timer(self, v):
        pass

    def timer(self, v):
        pass

    def _display(self):
        if self.grid_on:
            self.grid.draw()
        if self.axes_on:
            self.axes.draw()
        self.camera.update()

    def display(self):
        pass

    # ==========================================================================
    # Input callback implementations
    # ==========================================================================

    # --------------------------------------------------------------------------
    # keyboard
    #
    # - separate arrows from function keys
    # --------------------------------------------------------------------------

    def _keypress(self, key, x, y):
        """Default implementation of the `keypress callback`.
        """
        if key == chr(27) or key == chr(120):
            # escape or x
            exit()
            return
        if key == chr(43):
            # + (plus)
            self.camera.zoom_in()
            return
        if key == chr(45):
            # - (minus)
            self.camera.zoom_out()
            return

    def keypress(self, key, x, y):
        """Redefine this method to customise what the viewer does when specific
        keys are pressed.
        """
        pass

    def _special(self, key, x, y):
        """Default implementation of the `special keypress callback`.
        """
        if key == GLUT_KEY_UP:
            if self._mod == GLUT_ACTIVE_SHIFT:
                self.camera.ty += self.camera.dt * 10.0
                return
            if self._mod == GLUT_ACTIVE_ALT:
                self.camera.rx -= self.camera.dr
                return
            if self._mod == GLUT_ACTIVE_ALT | GLUT_ACTIVE_SHIFT:
                self.camera.rx -= self.camera.dr * 10.0
                return
            self.camera.ty += self.camera.dt
            return
        if key == GLUT_KEY_DOWN:
            if self._mod == GLUT_ACTIVE_SHIFT:
                self.camera.ty -= self.camera.dt * 10.0
                return
            if self._mod == GLUT_ACTIVE_ALT:
                self.camera.rx += self.camera.dr
                return
            if self._mod == GLUT_ACTIVE_ALT | GLUT_ACTIVE_SHIFT:
                self.camera.rx += self.camera.dr * 10.0
                return
            self.camera.ty -= self.camera.dt
            return
        if key == GLUT_KEY_LEFT:
            if self._mod == GLUT_ACTIVE_SHIFT:
                self.camera.tx -= self.camera.dt * 10.0
                return
            if self._mod == GLUT_ACTIVE_ALT:
                self.camera.rz -= self.camera.dr
                return
            if self._mod == GLUT_ACTIVE_ALT | GLUT_ACTIVE_SHIFT:
                self.camera.rz -= self.camera.dr * 10.0
                return
            self.camera.tx -= self.camera.dt
            return
        if key == GLUT_KEY_RIGHT:
            if self._mod == GLUT_ACTIVE_SHIFT:
                self.camera.tx += self.camera.dt * 10.0
                return
            if self._mod == GLUT_ACTIVE_ALT:
                self.camera.rz += self.camera.dr
                return
            if self._mod == GLUT_ACTIVE_ALT | GLUT_ACTIVE_SHIFT:
                self.camera.rz += self.camera.dr * 10.0
                return
            self.camera.tx += self.camera.dt
            return

    def special(self, key, x, y):
        pass

    # --------------------------------------------------------------------------
    # mouseclicks
    # --------------------------------------------------------------------------

    def left_mouseclick(self, x, y):
        pass

    def middle_mouseclick(self, x, y):
        pass

    def right_mouseclick(self, x, y):
        pass

    # --------------------------------------------------------------------------
    # clicked mousemotions
    # --------------------------------------------------------------------------

    def left_mousemotion(self, x, y):
        x_diff = x - self.mouse.x_last
        y_diff = y - self.mouse.y_last
        self.mouse.x_last = x
        self.mouse.y_last = y
        self.camera.rx += self.camera.dr * y_diff
        self.camera.rz += self.camera.dr * x_diff

    # use mousewheel for zooming
    # see: https://www.opengl.org/documentation/specs/glut/spec3/node73.html

    def middle_mousemotion(self, x, y):
        pass

    def right_mousemotion(self, x, y):
        x_diff = x - self.mouse.x_last
        y_diff = y - self.mouse.y_last
        self.mouse.x_last = x
        self.mouse.y_last = y
        self.camera.tx += self.camera.dt * x_diff
        self.camera.ty -= self.camera.dt * y_diff

    # --------------------------------------------------------------------------
    # unclicked mousemotions
    # --------------------------------------------------------------------------

    def mousemotion(self, x, y):
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        y = viewport[3] - y
        z = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)[0][0]
        pos = gluUnProject(x, y, z, modelview, projection, viewport)
        # print(pos)

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def screenshot(self, filename):
        """"""
        width = self.width
        height = self.height
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGB", (width, height), pixels)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(filename)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    viewer = Viewer()
    viewer.setup()
    viewer.show()
