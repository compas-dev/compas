from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import json
import sys

from compas.base import Base
from compas.files.xml import XML
from compas.files.xml import XMLElement
from compas.utilities import memoize

__all__ = [
    'URDF',
    'URDFElement',
    'URDFParser',
]


def _tag_without_namespace(element, default_namespace):
    if not default_namespace:
        return element.tag

    default_namespace_prefix = '{{{}}}'.format(default_namespace)
    prefix, namespace, postfix = element.tag.partition(default_namespace_prefix)
    has_default_namespace = namespace == default_namespace_prefix

    tagname = postfix if has_default_namespace else prefix
    return tagname


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

    References
    ----------
    A detailed description of the model is available on the `URDF Model wiki`_.
    This package parses URDF v1.0 according to the `URDF XSD Schema`_.

    * `URDF`_
    * `URDF Model wiki`_
    * `URDF XSD Schema`_

    .. _URDF: http://wiki.ros.org/urdf
    .. _URDF Model wiki: http://wiki.ros.org/urdf/XML/model
    .. _URDF XSD Schema: https://github.com/ros/urdfdom/blob/master/xsd/urdf.xsd

    """

    def __init__(self, xml=None):
        self.xml = xml
        self._robot = None

    @property
    def robot(self):
        if self._robot is None:
            default_namespace = self.xml.root.attrib.get('xmlns')
            self._robot = URDFParser.parse_element(self.xml.root, _tag_without_namespace(self.xml.root, default_namespace), default_namespace)
        return self._robot

    @robot.setter
    def robot(self, robot):
        robot_element = robot.get_urdf_element()
        root = robot_element.get_root()
        robot_element.add_children(root)
        self.xml = XML()
        self.xml.root = root
        self._robot = robot

    @classmethod
    def from_robot(cls, robot):
        urdf = cls()
        urdf.robot = robot
        return urdf

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

    @classmethod
    def read(cls, source):
        """Parse a URDF file from a file path or file-like object.

        Parameters
        ----------
        source : str or file
            File path or file-like object.

        Examples
        --------
        >>> from compas.files import URDF
        >>> urdf = URDF.read('/urdf/ur5.urdf')
        """
        return cls.from_file(source)

    def to_file(self, destination=None, prettify=False):
        """Writes the string representation of this URDF instance,
        including all sub-elements, to the ``destination``.

        Parameters
        ----------
        destination : str, optional
            Filepath where the URDF should be written.  Defaults to
            the filepath of the associated XML object.
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        if destination:
            self.xml.filepath = destination
        self.xml.write(prettify=prettify)

    def to_string(self, encoding='utf-8', prettify=False):
        """Generate a string representation of this URDF instance,
        including all sub-elements.

        Parameters
        ----------
        encoding : str, optional
            Output encoding (the default is 'utf-8')
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        str
            String representation of the URDF.

        """
        return self.xml.to_string(encoding=encoding, prettify=prettify)

    def write(self, destination=None, prettify=False):
        """Writes the string representation of this URDF instance,
        including all sub-elements, to the ``destination``.

        Parameters
        ----------
        destination : str, optional
            Filepath where the URDF should be written.  Defaults to
            the filepath of the associated XML object.
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        self.to_file(destination=destination, prettify=prettify)


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
    def parse_element(cls, element, path='', element_default_namespace=None):
        """Recursively parse URDF element and its children.

        If the parser type implements a class method ``from_urdf``,
        it will use it to parse the element, otherwise
        a generic implementation that relies on conventions
        will be used.

        Parameters
        ----------
        element :
            XML Element node.
        path : str
            Full path to the element.
        element_default_namespace : str
            Default namespace at the current level current document.

        Returns
        -------
        object
            An instance of the model object represented by the given element.

        """
        default_ns = element.attrib.get('xmlns') or element_default_namespace
        children = []

        for child in element:
            default_ns = child.attrib.get('xmlns') or element_default_namespace
            child_name = _tag_without_namespace(child, default_ns)
            child_path = '/'.join([path, child_name])
            children.append(cls.parse_element(child, child_path, default_ns))

        parser_type = cls._parsers.get(path, None) or URDFGenericElement

        metadata = get_metadata(parser_type)

        attributes = dict(element.attrib)
        text = element.text.strip() if element.text else None

        try:
            if 'from_urdf' in metadata:
                obj = metadata['from_urdf'](attributes, children, text)
            else:
                obj = cls.from_generic_urdf(
                    parser_type, attributes, children, text, default_ns)
        except Exception as e:
            raise TypeError('Cannot create instance of %s. Message=%s' % (parser_type, e))

        obj._urdf_source = element

        return obj

    @classmethod
    def from_generic_urdf(cls, parser_type, attributes=None, children=None, text=None, default_namespace=None):
        kwargs = attributes
        kwargs.update(cls.build_kwargs_by_type(children, parser_type, default_namespace))

        return parser_type(**kwargs)

    @classmethod
    def filter_elements(cls, elements, type):
        return filter(lambda i: isinstance(i, type), elements)

    @classmethod
    def _argname_from_element(cls, element, metadata, default_namespace):
        init_args = metadata['init_args']

        # Match URDF tag to an argument name in the constructor
        urdf_tag = _tag_without_namespace(element._urdf_source, default_namespace)
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
    def build_kwargs_by_type(cls, elements, parser_type, default_namespace):
        result = dict()
        metadata = get_metadata(parser_type)

        for child in elements:
            key = cls._argname_from_element(child, metadata, default_namespace)

            if key in metadata['init_args'] and metadata['init_args'][key]['sequence']:
                itemlist = result.get(key, [])
                itemlist.append(child)
                result[key] = itemlist
            else:
                result[key] = child

        return result


class URDFGenericElement(Base):
    """Generic representation for all URDF elements that
    are not explicitly supported."""

    def get_urdf_element(self):
        if not (hasattr(self, '_urdf_source') or hasattr(self, 'tag')):
            raise Exception('No tag found for element {}'.format(self))
        tag = self.tag if hasattr(self, 'tag') else self._urdf_source.tag
        return URDFElement(tag, self.attr, self.elements, self.text)

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        el = cls()
        el.attr = attributes
        el.elements = elements
        el.text = text
        return el

    @property
    def data(self):
        return {
            'attr': self.attr,
            'elements': [d.data for d in self.elements],
            'text': self.text,
        }

    @data.setter
    def data(self, data):
        self.attr = data['attr']
        self.elements = [URDFGenericElement.from_data(d) for d in data['elements']]
        self.text = data['text']

    @classmethod
    def from_data(cls, data):
        generic = cls()
        generic.attr = data['attr']
        generic.elements = [cls.from_data(d) for d in data['elements']]
        generic.text = data['text']
        return generic

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)


class URDFElement(XMLElement):
    def __init__(self, tag, attributes=None, elements=None, text=None):
        elements = [e.get_urdf_element() for e in elements or [] if e is not None]
        super(URDFElement, self).__init__(tag, attributes, elements, text)
        self.redistribute_elements()

    def redistribute_elements(self):
        attributes = {}
        for key, value in self.attributes.items():
            if hasattr(value, 'get_urdf_element'):
                self.elements.append(value.get_urdf_element())
            else:
                attributes[key] = str(value)
        self.attributes = attributes


@memoize
def get_metadata(type):
    metadata = dict()

    if hasattr(type, 'from_urdf'):
        metadata['from_urdf'] = getattr(type, 'from_urdf')
    else:
        if sys.version_info[0] < 3:
            argspec = inspect.getargspec(type.__init__)  # this is deprecated in python3
        else:
            argspec = inspect.getfullargspec(type.__init__)
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
        if sys.version_info[0] < 3:
            metadata['keywords'] = argspec.keywords is not None
        else:
            # TODO: make sure replacing keyword with kwonlyargs is correct, check at: https://docs.python.org/3/library/inspect.html#inspect.getargspec
            metadata['keywords'] = argspec.kwonlyargs is not None
        metadata['init_args'] = args

    metadata['argument_map'] = getattr(type, 'argument_map', {})

    return metadata
