from compas_blender.utilities import clear_layer
from compas_blender.utilities import set_objects_location
from compas_blender.utilities import set_objects_show_name
from compas_blender.utilities import xdraw_mesh
from compas_blender.utilities import xdraw_spheres

from compas.hpc import length_vector_numba

from numpy import array
from numpy import hstack
from numpy import vstack

from numba import jit
from numba import float64
from numba import int64

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Assumptions

# 1) Planets' orbit are circular (they are slightly elliptic).
# 2) Planets' orbit are dominated by the Sun and not each other (decoupled).

clear_layer(layer=0)

# Constants

G = 6.67408 * 10**(-11)  # m^3 kg^-1 s^-2

giga = 10**9
mega = 10**6
kilo = 10**3
scale = 5

min = 60
hour = 60 * min
day = 24 * hour
year = 365 * day

# Planets data

planets_radius = [
    2440 * kilo,   # mercury
    6052 * kilo,   # venus
    6371 * kilo,   # earth
    3390 * kilo,   # mars
    69911 * kilo,  # jupiter
    58232 * kilo,  # saturn
    25362 * kilo,  # uranus
    24622 * kilo,  # neptune
    ]

planets_distance = [
    57.91 * giga,  # mercury
    108.2 * giga,  # venus
    149.6 * giga,  # earth
    227.9 * giga,  # mars
    778.5 * giga,  # jupiter
    1429. * giga,  # saturn
    2871. * giga,  # uranus
    4498. * giga,  # neptune
    ]

planets_mass = array([
    3.285 * 10**23,  # mercury
    4.867 * 10**24,  # venus
    5.972 * 10**24,  # earth
    6.390 * 10**23,  # mars
    1.898 * 10**27,  # jupiter
    55.68 * 10**26,  # saturn
    8.681 * 10**25,  # uranus
    1.024 * 10**26,  # neptune
])

planets_speed = [
    47.36 * kilo,  # mercury
    35.02 * kilo,  # venus
    29.80 * kilo,  # earth
    24.08 * kilo,  # mars
    13.07 * kilo,  # jupiter
    9.690 * kilo,  # saturn
    6.800 * kilo,  # uranus
    5.430 * kilo,  # neptune
]

planets_colour = [
    [0.3, 0.3, 0.3],  # mercury
    [1.0, 0.8, 0.0],  # venus
    [0.0, 0.0, 1.0],  # earth
    [1.0, 0.0, 0.0],  # mars
    [1.0, 0.5, 0.0],  # jupiter
    [1.0, 1.0, 0.0],  # saturn
    [0.4, 0.4, 1.0],  # uranus
    [0.0, 0.0, 0.6],  # neptune
]

planets_name = [
    'mercury',
    'venus',
    'earth',
    'mars',
    'jupiter',
    'saturn',
    'uranus',
    'neptune'
]

n = 8

# Planets

spheres = []
for c, name in enumerate(planets_name):
    location = planets_distance[c] / giga
    spheres.append({'name': name, 'radius': scale, 'pos': [0, location, 0], 'color': planets_colour[c]})
planets = xdraw_spheres(spheres)
set_objects_show_name(objects=planets)

# Sun

sun_radius = 695700 * kilo
sun_mass = 1.989 * 10**30
sun = xdraw_spheres([{'name': 'sun', 'pos': [0, 0, 0], 'radius': scale, 'color': [1, 1, 1]}])
set_objects_show_name(objects=sun)

# Initial conditions

x_sun = array([0., 0., 0.])
x_planets = array([[0, i, 0] for i in planets_distance])
v_planets = array([[i, 0, 0] for i in planets_speed])
xv_planets = hstack([x_planets, v_planets])
k = G * sun_mass * planets_mass

# Examples

dt = 10 * min
duration = 14 * year
refresh = 10
x_rocket = array([0 * giga, 880 * giga, 0.])
v_rocket = array([14000, -2400., 0.])

#dt = 10 * min
#duration = 120 * year
#refresh = 50
#x_rocket = array([600 * giga, 400 * giga, 0.])
#v_rocket = array([3000, -1997.2, 0.])

# Rocket

rocket_mass = 20000
xv_rocket = hstack([x_rocket, v_rocket])
rocket = xdraw_spheres([{'name': 'rocket', 'pos': list(x_rocket / giga), 'radius': scale, 'color': [0, 1, 0]}])[0]
m = G * sun_mass * rocket_mass
p = G * planets_mass * rocket_mass * 1


# Simulation

@jit(float64[:, :](int64, float64[:], float64[:, :], float64[:], float64, float64[:], float64, float64, float64, float64[:]), nogil=True, nopython=True)
def simulation(n, x_sun, xv_all, k, dt, planets_mass, rocket_mass, day, m, p):

    for j in range(int(day // dt)):

        # Planets

        for i in range(n):
            r = x_sun - xv_all[i, :3]
            d = length_vector_numba(r)
            c = k[i] / d**3
            Fx = c * r[0]
            Fy = c * r[1]
            Fz = c * r[2]
            xv_all[i, :3] += dt * xv_all[i, 3:]
            xv_all[i, 3] += dt * Fx / planets_mass[i]
            xv_all[i, 4] += dt * Fy / planets_mass[i]
            xv_all[i, 5] += dt * Fz / planets_mass[i]

        # Rocket - Sun

        r = x_sun - xv_all[n, :3]
        d = length_vector_numba(r)
        c = m / d**3
        Fx = c * r[0]
        Fy = c * r[1]
        Fz = c * r[2]

        # Rocket - Planets

        for i in range(n):
            r = xv_all[i, :3] - xv_all[n, :3]
            d = length_vector_numba(r)
            c = p[i] / d**3
            Fx += c * r[0]
            Fy += c * r[1]
            Fz += c * r[2]

        # Step

        xv_all[n, :3] += dt * xv_all[n, 3:]
        xv_all[n, 3] += dt * Fx / rocket_mass
        xv_all[n, 4] += dt * Fy / rocket_mass
        xv_all[n, 5] += dt * Fz / rocket_mass

    return xv_all


# Loop

xv_all = vstack([xv_planets, xv_rocket])

for i in range(duration // day):

    # Update day

    xv_all = simulation(n, x_sun, xv_all, k, dt, planets_mass, rocket_mass, day, m, p)

    # Plot

    if i % refresh == 0:
        locations = [list(loc) for loc in list(xv_all[:, :3] / giga)]
        set_objects_location(objects=planets, locations=locations[:8])
        set_objects_location(objects=[rocket], locations=[locations[8]])
        mesh = xdraw_mesh(name='path', vertices=[locations[8]])
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
