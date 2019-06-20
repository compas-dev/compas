import compas
from compas.datastructures import Mesh
from proxy import Proxy
import time

numerical = Proxy('compas.numerical', python='python')

# a proxy starts a server (server.py run as a subprocess)
# the server runs in the background
# to make requests
# send individual POST requests to the address of the background server
# always provide module, function, args, kwargs
# upon creation a proxy object attempts to
# reconnect to a running server if available at the provided address
# otherwise start a new server at the provided address
# ? stop the server when address is changed ?
#

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes({'is_anchor': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
mesh.update_default_edge_attributes({'q': 1.0})

for key, attr in mesh.vertices(True):
    attr['is_anchor'] = mesh.vertex_degree(key) == 2
    if key in (18, 35):
        attr['z'] = 5.0

k_i   = mesh.key_index()
xyz   = mesh.get_vertices_attributes(('x', 'y', 'z'))
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))
q     = mesh.get_edges_attribute('q')
fixed = mesh.vertices_where({'is_anchor': True})
fixed = [k_i[k] for k in fixed]
edges = [(k_i[u], k_i[v]) for u, v in mesh.edges()]

xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

print(xyz)
