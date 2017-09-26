from compas.datastructures.network import Network
from compas.numerical.methods.forcedensity import fd
import compas_tna.tna.algorithms as tna
from compas_tna.tna.diagrams.formdiagram import FormDiagram
from compas_tna.tna.diagrams.forcediagram import ForceDiagram
from compas.datastructures.network.algorithms import smooth_network_centroid
from compas.utilities import geometric_key


def make_gkdict(net):
    gkdict = {}
    for key in net.vertex:
        xyz = net.get_vertex_attributes(key, ['x', 'y', 'z'])
        gk = geometric_key(xyz=xyz, precision='4f')
        gkdict[gk] = key
    return gkdict

def network_smoothen_lines(lines, fixed):
    net = Network.from_lines(lines)
    fixed  =  []
    for vk in net.vertex:
        if net.vertex_degree(vk) == 1:
            fixed.append(vk)
    smooth_network_centroid(net, fixed)
    print net
    return net.to_lines()

def fd_network(net_data):
    network = Network.from_data(net_data)
    k_i   = network.key_index()
    xyz   = network.get_vertices_attributes(('x', 'y', 'z'))
    loads = network.get_vertices_attributes(('px', 'py', 'pz'))
    q     = network.get_edges_attribute('q')

    fixed = [k_i[k] for k in network if network.vertex[k]['is_anchor']]
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    for key in network:
        index = k_i[key]
        network.vertex[key]['x'] = xyz[index][0]
        network.vertex[key]['y'] = xyz[index][1]
        network.vertex[key]['z'] = xyz[index][2]
    return network.to_lines()

def make_tna_vault_max_z(form_lines, zmax, anchors):
    form = FormDiagram.from_lines(form_lines)
    gkdict = make_gkdict(form)

    for a in anchors:
        u = gkdict[geometric_key(a, precision='4f')]
        form.vertex[u]['is_anchor'] = True

    for key, attr in form.vertices_iter(True):
        if form.degree(key) <= 1:
            attr['is_anchor'] = True

    form.set_vertices_attribute('pz', 1.0)
    force = ForceDiagram.from_formdiagram(form)
    # tna.horizontal(form, force, alpha=100, kmax=200, display=False)
    tna.horizontal_nodal(form, force, alpha=100, kmax=5000, display=True)
    tna.vertical_from_zmax(form, force, zmax=zmax, density=1.0, display=False)
    return form.to_lines(), force.to_lines()


def horizontal_equilibrium(form, force, alpha, kmax):
    form = FormDiagram.from_data(form)
    force = ForceDiagram.from_data(force)
    # tna.horizontal(form, force, alpha=int(alpha), kmax=int(kmax), display=True)
    tna.horizontal_nodal(form, force, alpha=int(alpha), kmax=int(kmax), display=False)
    return form.to_data(), force.to_data()

def vertical_equilibrium(form, force, zmax, kmax):
    form = FormDiagram.from_data(form)
    force = ForceDiagram.from_data(force)
    tna.vertical_from_zmax(form, force, zmax=zmax, kmax=int(kmax), display=False)
    return form.to_data()


if __name__ == '__main__':
    # net = Network.from_json('pattern.json')
    # net = fd_network(net)
    # net.to_json('relaxed_net.json')
    form = FormDiagram.from_json('pattern.json')
    form, force = make_tna_vault_max_z(form)
    print form
    # form.to_json('floor.json')
    lines = form.to_lines()
    print lines
    print ''
    print ''
    lines = force.to_lines()
    print lines
