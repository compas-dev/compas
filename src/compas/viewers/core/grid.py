from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from compas.utilities import flatten

from compas.viewers.core.buffers import make_vertex_buffer
from compas.viewers.core.buffers import make_index_buffer


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Grid', ]


class Grid(object):
    """"""
    def __init__(self, x=10, y=10, linewidth=1, colour=(0.9, 0.9, 0.9), dotted=False):
        self.xlim = -x, x
        self.ylim = -y, y
        self.linewidth = linewidth
        self.colour = colour
        self.dotted = dotted

    def draw(self):
        glcolour3f(*self.colour)
        glLineWidth(self.linewidth)

        if self.dotted:
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, 0xAAAA)

        glBegin(GL_LINES)

        for i in range(self.xlim[0], self.xlim[1] + 1):
            if i == 0:
                glcolour3f(*self.colour)
                glVertex3f(i, self.ylim[0], 0)
                glVertex3f(i, 0, 0)
                glcolour3f(0.0, 1.0, 0.0)
                glVertex3f(i, 0, 0)
                glVertex3f(i, self.ylim[1], 0)
            else:
                glcolour3f(*self.colour)
                glVertex3f(i, self.ylim[0], 0)
                glVertex3f(i, self.ylim[1], 0)

        for i in range(self.ylim[0], self.ylim[1] + 1):
            if i == 0:
                glcolour3f(*self.colour)
                glVertex3f(self.xlim[0], i, 0)
                glVertex3f(0, i, 0)
                glcolour3f(1.0, 0.0, 0.0)
                glVertex3f(0, i, 0)
                glVertex3f(self.xlim[1], i, 0)
            else:
                glcolour3f(*self.colour)
                glVertex3f(self.xlim[0], i, 0)
                glVertex3f(self.xlim[1], i, 0)

        glEnd()

        if self.dotted:
            glDisable(GL_LINE_STIPPLE)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
