from compas_blender.utilities import clear_layer
from compas_blender.utilities import set_object_location
from compas_blender.utilities import set_objects_location
from compas_blender.utilities import set_objects_show_name
from compas_blender.utilities import xdraw_mesh
from compas_blender.utilities import xdraw_spheres

from compas.numerical import normrow

from numpy import array

import bpy
import bmesh


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
scale = 10

# Planets data

planets_radii = [
    2440 * kilo,  # mercury
    6052 * kilo,  # venus
    6371 * kilo,  # earth
    3390 * kilo,  # mars
    69911 * kilo, # jupiter
    58232 * kilo, # saturn
    25362 * kilo, # uranus 
    24622 * kilo, # neptune
    ]
    
planets_distance = [
    57.91 * giga,  # mercury
    108.2 * giga,  # venus
    149.6 * giga,  # earth
    227.9 * giga,  # mars
    778.5 * giga, # jupiter
    1429. * giga, # saturn
    2871. * giga, # uranus 
    4498. * giga, # neptune
    ]
    
planets_masses = [
    3.285 * 10**23 ,  # mercury
    4.867 * 10**24,  # venus
    5.972 * 10**24,  # earth
    6.39 * 10**23,  # mars
    1.898 * 10**27, # jupiter
    55.683 * 10**26, # saturn
    8.681 * 10**25, # uranus 
    1.024 * 10**26, # neptune
]

planets_speed = [
    47.36 * kilo,  # mercury
    35.02 * kilo,  # venus
    29.80 * kilo,  # earth
    24.08 * kilo,  # mars
    13.07 * kilo, # jupiter
    9.690 * kilo, # saturn
    6.800 * kilo, # uranus 
    5.430 * kilo, # neptune
]

# Planets spheres

planet_names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
planets = []
for c, name in enumerate(planet_names):
    planets.append({'name': name, 'radius': scale, 'pos': [0, planets_distance[c] / giga, 0]})
planets_spheres = xdraw_spheres(planets)

# Sun

sun_radius = 695700 * kilo
sun_mass = 1.989 * 10**30
sun_sphere = xdraw_spheres([{'name': 'sun', 'pos': [0, 0, 0], 'radius': scale}])

# Show name

set_objects_show_name(objects=planets_spheres + sun_sphere)

# Solver

min = 60
hour = 60 * min
day = 24 * hour
year = 365 * day

dt = 200 * min
plot = 1 * day
duration = 5 * year

# Initial conditions

x_sun = array([0, 0, 0])
x_planets = [array([0, distance, 0]) for distance in planets_distance]
v_planets = [array([speed, 0, 0]) for speed in planets_speed]

# Rocket

rocket_mass = 20000
#x_rocket = array([80 * giga, 920 * giga, 0.])
#v_rocket = array([12000, -2400., 0.])
x_rocket = array([560 * giga, 90 * giga, 0.])
v_rocket = array([1000, -9700., 0.])
rocket_sphere = xdraw_spheres([{'name': 'rocket', 'pos': list(x_rocket / giga), 'radius': scale, 'color': [1, 0, 0]}])[0]
x_previous = list(x_rocket / giga)

# Simulation

for step in range(duration // dt):
    
    # Time
  
    time = step * dt
    print('Step: {0}/{1}'.format(step, duration // dt))

    # Planets

    for i in range(len(planets)):
        r = x_sun - x_planets[i]
        rl = float(normrow(r))
        rn = r / rl
        F = (G * sun_mass * planets_masses[i] / rl**2) * rn
        x_planets[i] += dt * v_planets[i]
        v_planets[i] += dt * F / planets_masses[i]
        
    # Rocket - Sun

    r = x_sun - x_rocket
    rl = float(normrow(r))
    rn = r / rl
    F = (G * sun_mass * rocket_mass / rl**2) * rn

    # Rocket - Planets

    for i in range(len(planets)):
        r = x_planets[i] - x_rocket
        rl = float(normrow(r))
        rn = r / rl
        F += (G * rocket_mass * planets_masses[i] / rl**2) * rn

    # Rocket step
    
    x_rocket += dt * v_rocket
    v_rocket += dt * F / rocket_mass
        
    # Plot
        
    if time % plot == 0:
        
        locations = [list(i / giga) for i in x_planets]
        set_objects_location(objects=planets_spheres, locations=locations)
        
        x_new = list(x_rocket / giga)
        
        set_object_location(object=rocket_sphere, location=x_new)
        
        mesh = xdraw_mesh(name='path', vertices=[x_previous, x_new], edges=[[0, 1]])
        
        x_previous = [i for i in x_new]
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
