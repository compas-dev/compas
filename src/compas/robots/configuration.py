from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.base import Base
from compas.robots.model.joint import Joint

__all__ = [
    'Configuration',
    'FixedLengthList',
]


def joint_names_validator(joint_names, key=None, value=None):
    new_joint_names = list(joint_names)
    if key is not None and value is not None:
        new_joint_names.__setitem__(key, value)
    if len(new_joint_names) != len(set(new_joint_names)):
        raise ValueError('joint_names cannot have repeated values.')


class FixedLengthList(list):
    """Restriction of the standard Python list to prevent changes in length
    while maintaining the ability to change values.  An optional ``validator``
    can be passed to the constructor which would be used to validate changes
    to the values.

    Parameters
    ----------
    validator : :obj:`function`
        A boolean function with the same signature as __setiem__, ie
        validator(fll: FixedLengthList, key: slice, value: Any) -> bool
    """
    def __init__(self, *args, **kwargs):
        super(FixedLengthList, self).__init__(*args)
        self.validator = kwargs.get('validator')
        if self.validator:
            self.validator(self)

    def __setitem__(self, key, value):
        # included to obstruct the all too common `l[1:1] = range(100)`-type usage
        value_length = len(value) if hasattr(value, '__len__') else 1
        slice_length = len(range(*key.indices(self.__len__()))) if isinstance(key, slice) else 1
        if slice_length != value_length:
            raise TypeError('Cannot change length of FixedLengthList')
        if self.validator:
            self.validator(self, key, value)
        super(FixedLengthList, self).__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        # for ironpython
        slice_end = min(j, self.__len__())
        slice_length = slice_end - i
        value_length = len(sequence)
        if slice_length != value_length:
            raise TypeError('Cannot change length of FixedLengthList')
        if self.validator:
            self.validator(self, slice(i, j), sequence)
        super(FixedLengthList, self).__setslice__(i, j, sequence)

    def append(self, item): raise TypeError('Cannot change length of FixedLengthList')
    def extend(self, other): raise TypeError('Cannot change length of FixedLengthList')
    def insert(self, i, item): raise TypeError('Cannot change length of FixedLengthList')
    def remove(self, item): raise TypeError('Cannot change length of FixedLengthList')
    def pop(self, i=-1): raise TypeError('Cannot change length of FixedLengthList')
    def clear(self): raise TypeError('Cannot change length of FixedLengthList')


class Configuration(Base):
    """Represents the configuration of a robot based on the state of its joints.
    If the names of joints are also provided, the configuration behaves as a
    dictionary of joint name-value pairs.

    This concept is also refered to as \"Joint State\".

    Parameters
    ----------
    joint_values : :obj:`list` of :obj:`float`
        Joint values expressed in radians or meters, depending on the respective
        type.
    joint_types : :obj:`list` of :attr:`compas.robots.Joint.SUPPORTED_TYPES`
        Joint types, e.g. a list of :attr:`compas.robots.Joint.REVOLUTE` for
        revolute joints.
    joint_names : :obj:`list` of :obj:`str`, optional
        List of joint names.

    Attributes
    ----------
    joint_values : :obj:`list` of :obj:`float`
        Joint values expressed in radians or meters, depending on the respective
        type.
    joint_types : :obj:`list` of :attr:`compas.robots.Joint.SUPPORTED_TYPES`
        Joint types, e.g. a list of :attr:`compas.robots.Joint.REVOLUTE` for
        revolute joints.
    joint_names : :obj:`list` of :obj:`str`
        List of joint names.
    data : :obj:`dict`
        The data representing the configuration.
    prismatic_values : :obj:`list` of :obj:`float`
        Prismatic joint values in meters.
    revolute_values : :obj:`list` of :obj:`float`
        Revolute joint values in radians.

    Examples
    --------
    >>> config = Configuration.from_revolute_values([math.pi/2, 0., 0.])
    >>> config.joint_values
    [1.5707963267948966, 0.0, 0.0]

    >>> from compas_fab.robots import Configuration
    >>> config = Configuration.from_prismatic_and_revolute_values([8.312], [math.pi/2, 0., 0., 0., 2*math.pi, 0.8])
    >>> str(config)
    'Configuration((8.312, 1.571, 0.000, 0.000, 0.000, 6.283, 0.800), (2, 0, 0, 0, 0, 0, 0))'

    >>> from compas_fab.robots import Configuration
    >>> from compas.robots import Joint
    >>> config = Configuration([math.pi/2, 3., 0.1], [Joint.REVOLUTE, Joint.PRISMATIC, Joint.PLANAR])
    >>> str(config)
    'Configuration((1.571, 3.000, 0.100), (0, 2, 5))'

    """

    def __init__(self, joint_values=None, joint_types=None, joint_names=None):
        joint_values = FixedLengthList(joint_values or [])
        joint_types = FixedLengthList(joint_types or [])
        joint_names = FixedLengthList(joint_names or [], validator=joint_names_validator)

        if len(joint_values) != len(joint_types):
            raise ValueError('{} joint_values must have {} joint_types, but {} given.'.format(
                len(joint_values), len(joint_values), len(joint_types)))

        if joint_names and len(joint_names) != len(joint_values):
            raise ValueError('{} joint_values must have either 0 or {} names, but {} given'.format(
                len(joint_values), len(joint_values), len(joint_names)
            ))

        self._precision = '3f'
        self._joint_values = joint_values
        self._joint_types = joint_types
        self._joint_names = joint_names

    @property
    def joint_values(self):
        """Joint values expressed in radians or meters, depending on the respective
        type.

        Returns
        -------
        :obj:`list` of :obj:`float`
        """
        return self._joint_values

    @joint_values.setter
    def joint_values(self, values):
        if len(self._joint_values) != len(values):
            raise Exception('joint_values must have length {}, object of length {} given'.format(len(self._joint_values), len(values)))
        self._joint_values = FixedLengthList(values)

    @property
    def joint_types(self):
        """Joint joint_types, e.g. a list of :attr:`compas.robots.Joint.REVOLUTE` for
        revolute joints.

        Returns
        -------
        :obj:`list` of :attr:`compas.robots.Joint.SUPPORTED_TYPES`
        """
        return self._joint_types

    @joint_types.setter
    def joint_types(self, joint_types):
        if len(self._joint_types) != len(joint_types):
            raise Exception('joint_types must have length {}, object of length {} given'.format(len(self._joint_types), len(joint_types)))
        self._joint_types = FixedLengthList(joint_types)

    @property
    def joint_names(self):
        """"List of joint names.

        Returns
        -------
        :obj:`list` of :obj:`str`
        """
        return self._joint_names

    @joint_names.setter
    def joint_names(self, names):
        if names and len(self._joint_values) != len(names):
            raise ValueError('joint_types must have length {}, object of length {} given'.format(len(self._joint_values), len(names)))
        self._joint_names = FixedLengthList(names, validator=joint_names_validator)

    def __str__(self):
        """Return a human-readable string representation of the instance."""
        v_str = ('(' + ", ".join(['%.' + self._precision] * len(self.joint_values)) + ')') % tuple(self.joint_values)
        if len(self.joint_names):
            return "Configuration({}, {}, {})".format(v_str, tuple(self.joint_types), tuple(self.joint_names))
        else:
            return "Configuration({}, {})".format(v_str, tuple(self.joint_types))

    def __repr__(self):
        """Printable representation of :class:`Configuration`."""
        return self.__str__()

    def __getitem__(self, item):
        for name, value in zip(self.joint_names, self.joint_values):
            if name == item:
                return value
        raise KeyError(item)

    def __setitem__(self, item, value):
        i = self.joint_names.index(item)
        if i < 0:
            raise KeyError(item)
        self.joint_values[i] = value

    def __bool__(self):
        # If __bool__ is not overwritten, then calls to bool default to the value given by __len__.
        # Since __len__ should reflect the number of items given by iterating over the object,
        # __len__ returns len(self.joint_names).  However, there are valid Configurations that lack
        # joint names, and should not be falsy.
        return True

    def __nonzero__(self):
        # ironpython's version of __bool__
        return self.__bool__()

    def __len__(self):
        return len(self.joint_names)

    def __iter__(self):
        return iter(self.joint_names)

    def items(self):
        return zip(self.joint_names, self.joint_values)

    def keys(self):
        return iter(self.joint_names)

    def values(self):
        return iter(self.joint_values)

    def get(self, key, default=None):
        try:
            value = self[key]
        except KeyError:
            value = default
        return value

    @classmethod
    def from_revolute_values(cls, values, joint_names=None):
        """Construct a configuration from revolute joint values in radians.

        Parameters
        ----------
        values : :obj:`list` of :obj:`float`
            Joint values expressed in radians.
        joint_names : :obj:`list` of :obj:`str`, optional
            List of joint names.

        Returns
        -------
        :class:`Configuration`
             An instance of :class:`Configuration` instance.
        """
        values = list(values)
        joint_names = list(joint_names or [])
        return cls.from_data({'joint_values': values, 'joint_types': [Joint.REVOLUTE] * len(values), 'joint_names': joint_names})

    @classmethod
    def from_prismatic_and_revolute_values(cls, prismatic_values, revolute_values, joint_names=None):
        """Construct a configuration from prismatic and revolute joint values.

        Parameters
        ----------
        prismatic_values : :obj:`list` of :obj:`float`
            Positions on the external axis system in meters.
        revolute_values : :obj:`list` of :obj:`float`
            Joint values expressed in radians.
        joint_names : :obj:`list` of :obj:`str`, optional
            List of joint names.

        Returns
        -------
        :class:`Configuration`
             An instance of :class:`Configuration`.
        """
        # Force iterables into lists
        prismatic_values = list(prismatic_values)
        revolute_values = list(revolute_values)
        joint_names = list(joint_names or [])
        values = prismatic_values + revolute_values
        joint_types = [Joint.PRISMATIC] * \
            len(prismatic_values) + [Joint.REVOLUTE] * len(revolute_values)
        return cls.from_data({'joint_values': values, 'joint_types': joint_types, 'joint_names': joint_names})

    @classmethod
    def from_data(cls, data):
        """Construct a configuration from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`Configuration`
             An instance of :class:`Configuration`.
        """
        config = cls()
        config.data = data
        return config

    def to_data(self):
        """Get the data dictionary that represents the configuration.

        This data can also be used to reconstruct the :class:`Configuration`
        instance.

        Returns
        -------
        :obj:`dict`
            The data representing the configuration.
        """
        return self.data

    @property
    def data(self):
        """:obj:`dict` : The data representing the configuration.

        By assigning a data dictionary to this property, the current data of
        the configuration will be replaced by the data in the :obj:`dict`. The
        data getter and setter should always be used in combination with each
        other.
        """
        return {
            'joint_values': self.joint_values,
            'joint_types': self.joint_types,
            'joint_names': self.joint_names
        }

    @data.setter
    def data(self, data):
        self._joint_values = FixedLengthList(data.get('joint_values') or [])
        self._joint_types = FixedLengthList(data.get('joint_types') or [])
        self._joint_names = FixedLengthList(data.get('joint_names') or [])

    @property
    def prismatic_values(self):
        """:obj:`list` of :obj:`float` : Prismatic joint values in meters.

        E.g. positions on the external axis system.
        """
        return [v for i, v in enumerate(self.joint_values) if self.joint_types[i] == Joint.PRISMATIC]

    @property
    def revolute_values(self):
        """:obj:`list` of :obj:`float` : Revolute joint values in radians."""
        return [v for i, v in enumerate(self.joint_values) if self.joint_types[i] == Joint.REVOLUTE]

    def copy(self):
        """Create a copy of this :class:`Configuration`.

        Returns
        -------
        :class:`Configuration`
            An instance of :class:`Configuration`
        """
        cls = type(self)
        return cls(self.joint_values[:], self.joint_types[:], self.joint_names[:])

    def scale(self, scale_factor):
        """Scales the joint positions of the current configuration.

        Only scalable joints are scaled, i.e. planar and prismatic joints.

        Parameters
        ----------
        scale_factor : :obj:`float`
            Scale factor.

        Returns
        -------
        None
        """
        values_scaled = []

        for value, joint_type in zip(self.joint_values, self.joint_types):
            if joint_type in (Joint.PLANAR, Joint.PRISMATIC):
                value *= scale_factor
            values_scaled.append(value)

        self._joint_values = FixedLengthList(values_scaled)

    def scaled(self, scale_factor):
        """Return a scaled copy of this configuration.

        Only scalable joints are scaled, i.e. planar and prismatic joints.

        Parameters
        ----------
        scale_factor : :obj:`float`
            Scale factor

        Returns
        -------
        None
        """
        config = self.copy()
        config.scale(scale_factor)
        return config

    def iter_differences(self, other):
        """Generator over the differences to another `Configuration`'s joint_values.

        If the joint type is revolute or continuous, the smaller difference
        (+/- 2*:math:`\\pi`) is calculated.

        Parameters
        ----------
        other : :class:`Configuration`
            The configuration to compare to.

        Yields
        ------
        :obj:`float`
            The next difference to the `Configuration`'s joint_values.

        Raises
        ------
        ValueError
            If the configurations are not comparable.

        Examples
        --------
        >>> c1 = Configuration.from_revolute_values([1, 0, 3])
        >>> c2 = Configuration.from_revolute_values([1, 2 * pi, 4])
        >>> allclose(c1.iter_differences(c2), [0.0, 0.0, -1.0])
        True
        >>> c1 = Configuration.from_revolute_values([1, 0, 3])
        >>> c2 = Configuration.from_revolute_values([1, -2 * pi - 0.2, 4])
        >>> allclose(c1.iter_differences(c2), [0.0, 0.2, -1.0])
        True
        """
        if self.joint_names and other.joint_names:
            if set(self.joint_names) != set(other.joint_names):
                raise ValueError("Configurations have different joint names.")
            other_value_by_name = dict(zip(other.joint_names, other.joint_values))
            sorted_other_values = [other_value_by_name[name] for name in self.joint_names]
            value_pairs = zip(self.joint_values, sorted_other_values)
        else:
            if len(self.joint_values) != len(other.joint_values):
                raise ValueError("Can't compare configurations with different lengths of joint_values.")
            value_pairs = zip(self.joint_values, other.joint_values)

        for i, (v1, v2) in enumerate(value_pairs):
            diff = v1 - v2
            if self.joint_types[i] in [Joint.REVOLUTE, Joint.CONTINUOUS]:
                d1 = diff % (2 * pi)
                d1 = d1 if diff >= 0 else d1 - 2*pi
                d2 = d1 - 2*pi if diff >= 0 else d1 + 2*pi
                diff = d1 if abs(d1) < abs(d2) else d2
            yield diff

    def max_difference(self, other):
        """Returns the maximum difference to another `Configuration`'s joint values.

        Parameters
        ----------
        other : :class:`Configuration`
            The configuration to compare to.

        Returns
        ------
        :obj:`float`
            The maximum absolute difference.

        Examples
        --------
        >>> c1 = Configuration.from_revolute_values([1, 0, 3])
        >>> c2 = Configuration.from_revolute_values([1, 2 * pi, 4])
        >>> c1.max_difference(c2)
        1.0
        """
        return max([abs(v) for v in self.iter_differences(other)])

    def close_to(self, other, tol=1e-3):
        """Returns ``True`` if the other `Configuration`'s joint_values are within a certain range.

        Parameters
        ----------
        other : :class:`Configuration`
            The configuration to compare to.
        tol : float
            The tolerance under which we consider 2 floats the same. Defaults to 1e-3.

        Returns
        -------
        :obj:`bool`
            ``True`` if the other `Configuration`'s joint_values are within a certain
            tolerance, `False` otherwise.

        Examples
        --------
        >>> c1 = Configuration.from_revolute_values([1, 0, 3])
        >>> c2 = Configuration.from_revolute_values([1, 2 * pi, 3])
        >>> c1.close_to(c2)
        True
        """
        for diff in self.iter_differences(other):
            if abs(diff) > tol:
                return False
        return True

    @property
    def has_joint_names(self):
        """Returns ``True`` when there is a joint name for every value."""
        return len(self.joint_values) == len(self.joint_names)

    def check_joint_names(self):
        """Raises an error if there is not a joint name for every value."""
        if not self.has_joint_names:
            if not len(self.joint_names):
                raise ValueError('Joint names are required for this operation.')
            else:
                raise ValueError('Joint names do not match the number of joint values. Joint names={}, Joint values={}'.format(len(self.joint_values), len(self.joint_names)))

    @property
    def joint_dict(self):
        """A dictionary of joint values by joint name."""
        self.check_joint_names()
        return dict(zip(self.joint_names, self.joint_values))

    @property
    def type_dict(self):
        """A dictionary of joint types by joint name."""
        self.check_joint_names()
        return dict(zip(self.joint_names, self.joint_types))

    def merge(self, other):
        """Merge the configuration with another configuration in place along joint names.
        The other configuration takes precedence over this configuration in
        case a joint value is present in both.

        Note
        ----
            Caution: ``joint_names`` may be rearranged.

        Parameters
        ----------
        other : :class:`Configuration`
            The configuration to be merged.

        Raises
        ------
        :exc:`ValueError`
            If the configuration or the ``other`` configuration does not specify
            joint names for all joint values.
        """
        _joint_dict = self.joint_dict
        _joint_dict.update(other.joint_dict)

        _type_dict = self.type_dict
        _type_dict.update(other.type_dict)

        self.joint_names = list(_joint_dict.keys())
        self.joint_values = [_joint_dict[name] for name in self.joint_names]
        self.joint_types = [_type_dict[name] for name in self.joint_names]

    def merged(self, other):
        """Get a new ``Configuration`` with this configuration merged with another configuration.
        The other configuration takes precedence over this configuration in
        case a joint value is present in both.

        Note
        ----
            Caution: ``joint_names`` may be rearranged.

        Parameters
        ----------
        other : :class:`Configuration`
            The configuration to be merged.

        Returns
        -------
        :class:`Configuration`
            A configuration with values for all included joints.

        Raises
        ------
        :exc:`ValueError`
            If the configuration or the ``other`` configuration does not specify
            joint names for all joint values.
        """
        _joint_dict = self.joint_dict
        _joint_dict.update(other.joint_dict)

        _type_dict = self.type_dict
        _type_dict.update(other.type_dict)

        joint_names = list(_joint_dict.keys())
        joint_values = [_joint_dict[name] for name in joint_names]
        joint_types = [_type_dict[name] for name in joint_names]

        return Configuration(joint_values, joint_types, joint_names)
