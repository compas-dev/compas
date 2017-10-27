# ==============================================================================
# An implementation of DR
# that simply resolves the residual forces at the nodes
# by moving along a damped residual force/movement vector.
# ==============================================================================


# class ForceNetwork(object):

#     # def __init__(self):
#     #     super(ForceNetwork, self).__init__()
#     #     self.update_default_vertex_attributes({
#     #         'p' : [0.0, 0.0, 0.0],
#     #         'v' : [0.0, 0.0, 0.0],
#     #     })
#     #     self.update_default_edge_attributes({})
#     #     self.dt = 1.0

#     def mass(self, key):
#         t = self.dt
#         m = 0.0
#         for nbr in self.vertex_neighbours(key):
#             q = self.get_edge_attribute((key, nbr), 'q')
#             m += 0.5 * t ** 2 * q
#         m = m or 1.0
#         return m

#     def residual(self, key, key_xyz, b, dt=1.0):
#         """Compute the residual force at a vertex with respect to a specific state
#         of the geometry.
#         """
#         nbrs = self.vertex_neighbours(key)

#         # get the coordinates of the node in the frozen geometric state
#         x0, y0, z0 = key_xyz[key]

#         # get the load on the node
#         px, py, pz = self.vertex[key]['p']

#         # initialise the components of the residual force at the node
#         # with the components of the external load
#         rx, ry, rz = px, py, pz

#         for nbr in nbrs:
#             # make sure all edges are from the node to its neighbours
#             if nbr in self.edge[key]:
#                 u, v = key, nbr
#             else:
#                 u, v = nbr, key

#             # get the coordinates of the neighbour
#             # in the frozen geometric state
#             xn, yn, zn = key_xyz[nbr]

#             # compute the length of the vector from the node to the neighbour
#             l = sqrt((xn - x0) ** 2 + (yn - y0) ** 2 + (zn - z0) ** 2)

#             # get the force density of the edge
#             q = self.edge[u][v]['q']

#             # compute the force in the connected edge
#             f = q * l

#             # compute the components of the force vector
#             fx = f * (xn - x0) / l
#             fy = f * (yn - y0) / l
#             fz = f * (zn - z0) / l

#             # add the internal forces to the residual force
#             rx += fx
#             ry += fy
#             rz += fz

#         # set the mass to 1.0 if the mass is zero
#         m = self.mass(key)

#         # compute the acceleration of the point
#         # by dividing the residual force vector by the mass of the node
#         ax = rx / m
#         ay = ry / m
#         az = rz / m

#         return ax, ay, az


# def dr(network, kmax=100, dt=1.0, tol1=1e-3, tol2=1e-6, c=0.1):
#     a = (1 - c * 0.5) / (1 + c * 0.5)
#     b = 0.5 * (1 + a)

#     network.dt = dt

#     fixed = set([key for key in network.vertices() if network.vertex[key]['is_fixed']])

#     for k in range(kmax):
#         key_xyz = {key: network.vertex_coordinates(key) for key in network.vertices()}

#         for key, attr in network.vertices(True):

#             if key in fixed:
#                 continue

#             rx, ry, rz = network.residual(key, key_xyz, b)

#             attr['x'] += c * rx
#             attr['y'] += c * ry
#             attr['z'] += c * rz
