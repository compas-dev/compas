from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from matplotlib.patches import Circle
from matplotlib.patches import Polygon

from compas.utilities import valuedict
from compas.utilities import color_to_rgb
from compas.utilities import pairwise

from compas.plotters.plotter import Plotter


__all__ = ['MeshPlotter']


class MeshPlotter(Plotter):
    """Definition of a plotter object based on matplotlib for compas Networks.

    Parameters
    ----------
    mesh: object
        The mesh to plot.

    Attributes
    ----------
    title : str
        Title of the plot.
    mesh : object
        The mesh to plot.
    vertexcollection : object
        The matplotlib collection for the mesh vertices.
    edgecollection : object
        The matplotlib collection for the mesh edges.
    facecollection : object
        The matplotlib collection for the mesh faces.
    defaults : dict
        Dictionary containing default attributes for vertices and edges.

        * vertex.radius    : ``0.1``
        * vertex.facecolor : ``'#ffffff'``
        * vertex.edgecolor : ``'#000000'``
        * vertex.edgewidth : ``0.5``
        * vertex.textcolor : ``'#000000'``
        * vertex.fontsize  : ``10``
        * edge.width       : ``1.0``
        * edge.color       : ``'#000000'``
        * edge.textcolor   : ``'#000000'``
        * edge.fontsize    : ``10``
        * face.facecolor   : ``'#eeeeee'``
        * face.edgecolor   : ``'#000000'``
        * face.edgewidth   : ``0.1``
        * face.textcolor   : ``'#000000'``
        * face.fontsize    : ``10``

    Examples
    --------
    This is a basic example using the default settings for all visualisation options.
    For more detailed examples, see the documentation of the various drawing methods
    listed below...

    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text='key', radius=0.15)
        plotter.draw_edges()
        plotter.draw_faces()

        plotter.show()

    Notes
    -----
    For more info about ``matplotlib``, see [1]_.

    References
    ----------
    .. [1] Hunter, J. D., 2007. *Matplotlib: A 2D graphics environment*.
           Computing In Science & Engineering (9) 3, p.90-95.
           Available at: http://ieeexplore.ieee.org/document/4160265/citations.

    """

    def __init__(self, mesh, **kwargs):
        """Initialises a mesh plotter object"""
        super(MeshPlotter, self).__init__(**kwargs)
        self.title = 'MeshPlotter'
        self.mesh = mesh
        self.vertexcollection = None
        self.edgecollection = None
        self.facecollection = None
        self.defaults = {
            'vertex.radius'    : 0.1,
            'vertex.facecolor' : '#ffffff',
            'vertex.edgecolor' : '#000000',
            'vertex.edgewidth' : 0.5,
            'vertex.textcolor' : '#000000',
            'vertex.fontsize'  : kwargs.get('fontsize', 10),

            'edge.width'    : 1.0,
            'edge.color'    : '#000000',
            'edge.textcolor': '#000000',
            'edge.fontsize' : kwargs.get('fontsize', 10),

            'face.facecolor' : '#eeeeee',
            'face.edgecolor' : '#000000',
            'face.edgewidth' : 0.1,
            'face.textcolor' : '#000000',
            'face.fontsize' : kwargs.get('fontsize', 10),
        }

    def clear(self):
        """Clears the mesh plotter vertices, edges and faces."""
        self.clear_vertices()
        self.clear_edges()
        self.clear_faces()

    def draw_vertices(self,
                      keys=None,
                      radius=None,
                      text=None,
                      facecolor=None,
                      edgecolor=None,
                      edgewidth=None,
                      textcolor=None,
                      fontsize=None,
                      picker=None):
        """Draws the mesh vertices.

        Parameters
        ----------
        keys : list
            The keys of the vertices to plot.
        radius : list
            A list of radii for the vertices.
        text : list
            Strings to be displayed on the vertices.
        facecolor : list
            Color for the vertex circle fill.
        edgecolor : list
            Color for the vertex circle edge.
        edgewidth : list
            Width for the vertex circle edge.
        textcolor : list
            Color for the text to be displayed on the vertices.
        fontsize : list
            Font size for the text to be displayed on the vertices.

        Returns
        -------
        object
            The matplotlib vertex collection object.
        """
        keys = keys or list(self.mesh.vertices())

        if text == 'key':
            text = {key: str(key) for key in self.mesh.vertices()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.mesh.vertices())}
        elif isinstance(text, basestring):
            if text in self.mesh.default_vertex_attributes:
                default = self.mesh.default_vertex_attributes[text]
                if isinstance(default, float):
                    text = {key: '{:.1f}'.format(attr[text]) for key, attr in self.mesh.vertices(True)}
                else:
                    text = {key: str(attr[text]) for key, attr in self.mesh.vertices(True)}
        else:
            pass

        radiusdict    = valuedict(keys, radius, self.defaults['vertex.radius'])
        textdict      = valuedict(keys, text, '')
        facecolordict = valuedict(keys, facecolor, self.defaults['vertex.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.defaults['vertex.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.defaults['vertex.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.defaults['vertex.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['vertex.fontsize'])

        points = []
        for key in keys:
            points.append({
                'pos'      : self.mesh.vertex_coordinates(key, 'xy'),
                'radius'   : radiusdict[key],
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_points(points)
        self.vertexcollection = collection

        if picker:
            collection.set_picker(picker)
        return collection

    def clear_vertices(self):
        """Clears the mesh plotter vertices."""
        if self.vertexcollection:
            self.vertexcollection.remove()

    def update_vertices(self, radius=None):
        """Updates the plotter vertex collection based on the current state of the mesh.

        Parameters
        ----------
        radius : {float, dict}, optional
            The vertex radius as a single value, which will be applied to all vertices,
            or as a dictionary mapping vertex keys to specific radii.
            Default is the value set in ``self.defaults``.

        Note
        ----
        This function will only work as expected if all vertices were already present in the collection.

        Examples
        --------
        .. code-block:: python

            pass

        """
        radius = valuedict(self.mesh.vertices(), radius, self.defaults['vertex.radius'])
        circles = []
        for key in self.mesh.vertices():
            c = self.mesh.vertex_coordinates(key, 'xy')
            r = radius[key]
            circles.append(Circle(c, r))
        self.vertexcollection.set_paths(circles)

    def draw_as_lines(self, color=None, width=None):
        """Draw the mesh as a set of lines.

        This function is useful for creating *before-after* plots.

        Parameters
        ----------
        color : {rgb-tuple, hex-string}, optional
            The color specification of the lines.
            Default is to use the default line color as defined in ``self.defaults``.
        width : float, optional
            The width of the lines.
            Default is to use the value specified in self.defaults.

        Returns
        -------
        object
            The ``matplotlib`` line collection object.

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            plotter = MeshPlotter(mesh)

            plotter.draw_as_lines()

            # do stuff to the mesh

            plotter.draw_vertices()
            plotter.draw_edges()

            plotter.show()

        """
        lines = []
        for u, v in self.mesh.edges():
            lines.append({
                'start' : self.mesh.vertex_coordinates(u, 'xy'),
                'end'   : self.mesh.vertex_coordinates(v, 'xy'),
                'color' : color,
                'width' : width,
            })
        return super(MeshPlotter, self).draw_lines(lines)

    def draw_edges(self,
                   keys=None,
                   width=None,
                   color=None,
                   text=None,
                   textcolor=None,
                   fontsize=None):
        """Draws the mesh edges.

        Parameters
        ----------
        keys : list
            The keys of the edges to plot.
        width : list
            Width of the mesh edges.
        color : list
            Color for the edge lines.
        text : list
            Strings to be displayed on the edges.
        textcolor : list
            Color for the text to be displayed on the edges.
        fontsize : list
            Font size for the text to be displayed on the edges.

        Returns
        -------
        object
            The matplotlib edge collection object.

        """
        keys = keys or list(self.mesh.edges())

        if text == 'key':
            text = {(u, v): '{}-{}'.format(u, v) for u, v in self.mesh.edges()}
        elif text == 'index':
            text = {(u, v): str(index) for index, (u, v) in enumerate(self.mesh.edges())}
        else:
            pass

        widthdict     = valuedict(keys, width, self.defaults['edge.width'])
        colordict     = valuedict(keys, color, self.defaults['edge.color'])
        textdict      = valuedict(keys, text, '')
        textcolordict = valuedict(keys, textcolor, self.defaults['edge.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['edge.fontsize'])

        lines = []
        for u, v in keys:
            lines.append({
                'start'    : self.mesh.vertex_coordinates(u, 'xy'),
                'end'      : self.mesh.vertex_coordinates(v, 'xy'),
                'width'    : widthdict[(u, v)],
                'color'    : colordict[(u, v)],
                'text'     : textdict[(u, v)],
                'textcolor': textcolordict[(u, v)],
                'fontsize' : fontsizedict[(u, v)]
            })

        collection = self.draw_lines(lines)
        self.edgecollection = collection
        return collection

    def clear_edges(self):
        """Clears the mesh plotter edges."""
        if self.edgecollection:
            self.edgecollection.remove()

    def update_edges(self):
        """Updates the plotter edge collection based on the mesh."""
        segments = []
        for u, v in self.mesh.edges():
            segments.append([self.mesh.vertex_coordinates(u, 'xy'), self.mesh.vertex_coordinates(v, 'xy')])
        self.edgecollection.set_segments(segments)

    def highlight_path(self, path, edgecolor=None, edgetext=None, edgewidth=None):
        lines = []
        for u, v in pairwise(path):
            sp = self.mesh.vertex_coordinates(u, 'xy')
            ep = self.mesh.vertex_coordinates(v, 'xy')
            lines.append({
                'start' : sp,
                'end'   : ep,
                'width' : edgewidth or self.defaults.get('edge.width', 2.0),
                'color' : edgecolor or self.defaults.get('edge.color', '#ff0000')
            })
        self.draw_lines(lines)

    def draw_faces(self,
                   keys=None,
                   text=None,
                   facecolor=None,
                   edgecolor=None,
                   edgewidth=None,
                   textcolor=None,
                   fontsize=None):
        """Draws the mesh faces.

        Parameters
        ----------
        keys : list
            The keys of the edges to plot.
        text : list
            Strings to be displayed on the edges.
        facecolor : list
            Color for the face fill.
        edgecolor : list
            Color for the face edge.
        edgewidth : list
            Width for the face edge.
        textcolor : list
            Color for the text to be displayed on the edges.
        fontsize : list
            Font size for the text to be displayed on the edges.

        Returns
        -------
        object
            The matplotlib face collection object.
        """
        keys = keys or list(self.mesh.faces())

        if text == 'key':
            text = {key: str(key) for key in self.mesh.faces()}
        elif text == 'index':
            text = {key: str(index) for index, key in enumerate(self.mesh.faces())}
        else:
            pass

        textdict      = valuedict(keys, text, '')
        facecolordict = valuedict(keys, facecolor, self.defaults['face.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.defaults['face.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.defaults['face.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.defaults['face.textcolor'])
        fontsizedict  = valuedict(keys, fontsize, self.defaults['face.fontsize'])

        polygons = []
        for key in keys:
            polygons.append({
                'points'   : self.mesh.face_coordinates(key, 'xy'),
                'text'     : textdict[key],
                'facecolor': facecolordict[key],
                'edgecolor': edgecolordict[key],
                'edgewidth': edgewidthdict[key],
                'textcolor': textcolordict[key],
                'fontsize' : fontsizedict[key]
            })

        collection = self.draw_polygons(polygons)
        self.facecollection = collection
        return collection

    def clear_faces(self):
        """Clears the mesh plotter faces."""
        if self.facecollection:
            self.facecollection.remove()

    def update_faces(self, facecolor=None):
        """Updates the plotter face collection based on the mesh."""
        facecolor = valuedict(self.mesh.faces(), facecolor, self.defaults['face.facecolor'])
        polygons = []
        facecolors = []
        for fkey in self.mesh.faces():
            points = self.mesh.face_coordinates(fkey, 'xy')
            polygons.append(Polygon(points))
            facecolors.append(color_to_rgb(facecolor[fkey], normalize=True))
        self.facecollection.set_paths(polygons)
        self.facecollection.set_facecolor(facecolors)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    plotter = MeshPlotter(mesh, figsize=(10, 6))

    plotter.draw_vertices(text='key', radius=0.2, picker=10)

    for text in plotter.axes.texts:
        text.set_visible(False)

    plotter.draw_edges()
    plotter.draw_faces()

    def onpick(event):
        index = event.ind[0]
        for i, text in enumerate(plotter.axes.texts):
            if i == index:
                text.set_visible(True)
            else:
                text.set_visible(False)
        plotter.update()

    plotter.register_listener(onpick)
    plotter.show()
