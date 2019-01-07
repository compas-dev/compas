from compas.utilities import color_to_colordict

import compas_rhino


__all__ = ['VertexArtist']


class VertexArtist(object):

    __module__ = "compas_rhino.artists.mixins"

    def clear_vertices(self, keys=None):
        """Clear all vertices previously drawn by the ``VertexArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertices that should be cleared.
            Default is to clear all vertices.

        """
        if not keys:
            name = '{}.vertex.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = self.datastructure.vertex_name(key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def clear_vertexlabels(self, keys=None):
        """Clear all vertex labels previously drawn by the ``VertexArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertex labels that should be cleared.
            Default is to clear all vertex labels.

        """
        if not keys:
            name = '{}.vertex.label.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = self.datastructure.vertex_label_name(key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default vertex
            color (``self.defaults['color.vertex']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        Notes
        -----
        The vertices are named using the following template:
        ``"{}.vertex.{}".format(self.datastructure.name], key)``.
        This name is used afterwards to identify vertices in the Rhino model.

        """
        keys = keys or list(self.datastructure.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.defaults.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for key in keys:
            points.append({
                'pos'   : self.datastructure.vertex_coordinates(key),
                'name'  : self.datastructure.vertex_name(key),
                'color' : colordict[key],
                'layer' : self.datastructure.get_vertex_attribute(key, 'layer', None)
            })
        return compas_rhino.xdraw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as key-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to vertex keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default vertex color (``self.defaults['color.vertex']``).

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.vertex.label.{}".format(self.datastructure.name, key)``.

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.vertices()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.defaults.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for key, text in iter(textdict.items()):
            labels.append({
                'pos'  : self.datastructure.vertex_coordinates(key),
                'name' : self.datastructure.vertex_label_name(key),
                'color': colordict[key],
                'text' : textdict[key],
                'layer' : self.datastructure.get_vertex_attribute(key, 'layer', None)
            })

        return compas_rhino.xdraw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
