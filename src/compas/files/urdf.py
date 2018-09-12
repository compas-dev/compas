from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import inspect

from compas.files.xml import XML
from compas.utilities import memoize

__all__ = [
    'URDF',
    'URDFParser'
]


class URDF(object):
    """Parse URDF files.

    This class abstracts away the underlying XML of the Unified Robot
    Description Format (`URDF`_) and represents its as an object graph.

    Attributes
    ----------
    xml : :class:`XML`
        Instance of the XML reader/parser class.
    robot : object
        Root element of the URDF model, i.e. a robot instance.

    See Also
    --------

    A detailed description of the model is available on the `URDF Model wiki`_.
    This package parses URDF v1.0 according to the `URDF XSD Schema`_.

    * `URDF`_
    * `URDF Model wiki`_
    * `URDF XSD Schema`_

    .. _URDF: http://wiki.ros.org/urdf
    .. _URDF Model wiki: http://wiki.ros.org/urdf/XML/model
    .. _URDF XSD Schema: https://github.com/ros/urdfdom/blob/master/xsd/urdf.xsd

    """
    def __init__(self, xml):
        self.xml = xml
        self.robot = URDFParser.parse_element(xml.root, xml.root.tag)

    @classmethod
    def from_file(cls, source):
        """Parse a URDF file from a file path or file-like object.

        Parameters
        ----------
        source : str or file
            File path or file-like object.

        Examples
        --------

        >>> from compas.files import URDF
        >>> urdf = URDF.from_file('/urdf/ur5.urdf')
        """
        return cls(XML.from_file(source))

    @classmethod
    def from_string(cls, text):
        """Parse URDF from a string.

        Parameters
        ----------
        text : :obj:`str`
            XML string.

        Examples
        --------

        >>> from compas.files import URDF
        >>> urdf = URDF.from_string('<robot name="panda"/>')
        """
        return cls(XML.from_string(text))


class URDFParser(object):
    """Parse URDF elements into an object graph."""
    _parsers = dict()

    @classmethod
    def install_parser(cls, parser_type, *tags):
        """Installs an URDF parser type for a defined tag.

        Parameters
        ----------
        parser_type : type
            Python class handling URDF parsing of the tag.
        tags : str
            One or more URDF string tag that the parser can parse.
        """
        if len(tags) == 0:
            raise ValueError('Must define at least one tag')

        for tag in tags:
            cls._parsers[tag] = parser_type

    @classmethod
    def parse_element(cls, element, path=''):
        """Recursively parse URDF element and its children.

        If the parser type implements a class method ``from_urdf``,
        it will use it to parse the elemenet, otherwise
        a generic implementation that relies on conventions
        will be used.

        Parameters
        ----------
        element :
            XML Element node.
        path : str
            Full path to the element.

        Returns
        -------
        object
            An instance of the model object represented by the given element.

        """
        children = [cls.parse_element(child, '/'.join([path, child.tag])) for child in element]
        parser_type = cls._parsers.get(path, None) or URDFGenericElement

        metadata = get_metadata(parser_type)

        attributes = dict(element.attrib)
        text = element.text.strip() if element.text else None

        try:
            if 'from_urdf' in metadata:
                obj = metadata['from_urdf'](attributes, children, text)
            else:
                obj = cls.from_generic_urdf(
                    parser_type, attributes, children, text)
        except Exception as e:
            raise TypeError('Cannot create instance of %s. Message=%s' % (parser_type, e))

        obj._urdf_source = element

        return obj

    @classmethod
    def from_generic_urdf(cls, parser_type, attributes=None, children=None, text=None):
        kwargs = attributes
        kwargs.update(cls.build_kwargs_by_type(children, parser_type))

        return parser_type(**kwargs)

    @classmethod
    def filter_elements(cls, elements, type):
        return filter(lambda i: isinstance(i, type), elements)

    @classmethod
    def _argname_from_element(cls, element, metadata):
        init_args = metadata['init_args']

        # Match URDF tag to an argument name in the constructor
        urdf_tag = element._urdf_source.tag
        if urdf_tag in init_args:
            return urdf_tag

        # Simplistic sequence matching based on pluralization
        plural_tag = '%ss' % urdf_tag
        if plural_tag in init_args:
            init_args['sequence'] = True
            return plural_tag

        argument_name = metadata['argument_map'].get(urdf_tag, None)
        if argument_name:
            return argument_name

        if metadata['keywords']:
            return urdf_tag

        raise ValueError('Cannot find a matching argument for %s' % urdf_tag)

    @classmethod
    def build_kwargs_by_type(cls, elements, parser_type):
        result = dict()
        metadata = get_metadata(parser_type)

        for child in elements:
            key = cls._argname_from_element(child, metadata)

            if key in metadata['init_args'] and metadata['init_args'][key]['sequence']:
                itemlist = result.get(key, [])
                itemlist.append(child)
                result[key] = itemlist
            else:
                result[key] = child

        return result


class URDFGenericElement(object):
    """Generic representation for all URDF elements that
    are not explicitely supported."""

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        el = cls()
        el.attr = attributes
        el.elements = elements
        el.text = text
        return el


@memoize
def get_metadata(type):
    metadata = dict()

    if hasattr(type, 'from_urdf'):
        metadata['from_urdf'] = getattr(type, 'from_urdf')
    else:
        argspec = inspect.getargspec(type.__init__)
        args = {}

        required = len(argspec.args)
        if argspec.defaults:
            required -= len(argspec.defaults)

        for i in range(1, len(argspec.args)):
            data = dict(required=i < required)
            default_index = i - required

            if default_index >= 0:
                default = argspec.defaults[default_index]
                data['default'] = default
                data['sequence'] = hasattr(default, '__iter__')
            else:
                data['sequence'] = False

            args[argspec.args[i]] = data

        metadata['keywords'] = argspec.keywords is not None
        metadata['init_args'] = args

    metadata['argument_map'] = getattr(type, 'argument_map', {})

    return metadata
