import compas_rhino

from compas.datastructures import Network
from compas.com import MatlabClient

# connect to the MATLAB COM automation server

matlab = MatlabClient()

# make a network from line geometry

guids = compas_rhino.select_lines()
lines = compas_rhino.get_line_coordinates(guids)

network = Network.from_lines(lines)

# vertex coordinates

xyz = network.get_vertices_attributes('xyz')
xyz = matlab.matrix_from_list(xyz)

# connectivity matrix

m, n = network.number_of_edges(), network.number_of_vertices()
key_index = network.key_index()

C = [[0] * n for _ in range(m)]

for i, (u, v) in enumerate(network.edges()):
    j, k = key_index[u], key_index[v]
    C[i][j] = -1
    C[i][k] = +1

C = matlab.matrix_from_list(C)

# put the matrices in the MATLAB workspace

matlab.put('xyz', xyz)
matlab.put('C', C)

# compute coordinate differences
# compute edge lengths

matlab.eval('uv = C * xyz;')
matlab.eval('l = sqrt(sum(uv .^ 2, 2));')

# get the result back

l = matlab.get('l')

# visualise lenghts as edge labels

compas_rhino.network_draw_edge_labels(
    network,
    text={(u, v): '{:.1f}'.format(l[i][0]) for i, (u, v) in enumerate(network.edges())}
)
