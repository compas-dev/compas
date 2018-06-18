from compas_rhino.geometry import RhinoMesh
from compas_rhino.utilities import clear_layer

from compas.utilities import XFunc

from math import sin
from math import cos

import rhinoscriptsyntax as rs


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Input

guid = rs.ObjectsByLayer('Plane')[0]
rhinomesh = RhinoMesh(guid)
vertices, faces = rhinomesh.get_vertices_and_faces()
points = [[x, y, sin(x) * cos(y)] for x, y, z in vertices]

# Set-up XFunc

basedir = 'D:/compas-dev/examples/'
tmpdir = 'C:/Temp/'
xfunc = XFunc(basedir=basedir, tmpdir=tmpdir)

# Python

xfunc.funcname = 'hpc_normals_func.python_normals'
normals, toc1 = xfunc(points, offset=0.5)['data']
print('Python : {0:.6f} ms'.format(toc1 * 1000))

# Numba

xfunc.funcname = 'hpc_normals_func.numba_normals'
normals, toc2 = xfunc(points, offset=0.5)['data']
print('Numba : {0:.6f} ms'.format((toc2 * 1000)))

# Numpy

xfunc.funcname = 'hpc_normals_func.numpy_normals'
normals, toc3 = xfunc(points, offset=0.5)['data']
print('Numpy : {0:.6f} ms'.format(toc3 * 1000))

# Plot

clear_layer(name='Plots')
n = len(points)
plot1 = rs.AddMesh(vertices=points, face_vertices=faces, vertex_colors=[[255, 0, 0]] * n)
plot2 = rs.AddMesh(vertices=normals, face_vertices=faces, vertex_colors=[[0, 0, 255]] * n)
rs.ObjectLayer([plot1, plot2], 'Plots')
