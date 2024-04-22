from compas.plugins import pluggable
from compas.plugins import PluginNotInstalledError


@pluggable(category="factories")
def from_box(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_boolean_difference(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_boolean_intersection(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_boolean_union(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_brepfaces(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_cone(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_cylinder(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_curves(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_extrusion(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_iges(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_loft(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_mesh(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_native(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_pipe(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_plane(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_planes(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_polygons(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_sphere(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_sweep(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_step(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def from_torus(*args, **kwargs):
    raise PluginNotInstalledError


@pluggable(category="factories")
def new_brep(cls, *args, **kwargs):
    raise PluginNotInstalledError
