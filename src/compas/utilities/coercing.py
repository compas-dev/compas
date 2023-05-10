from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

from compas.data.coercion import coerce_sequence_of_list
from compas.data.coercion import coerce_sequence_of_tuple
from compas.data.validators import is_sequence_of_str
from compas.data.validators import is_sequence_of_int
from compas.data.validators import is_sequence_of_float
from compas.data.validators import is_sequence_of_tuple
from compas.data.validators import is_sequence_of_list
from compas.data.validators import is_sequence_of_dict
from compas.data.validators import is_sequence_of_iterable
from compas.data.validators import is_item_iterable


warnings.warn(
    "The coercing module in utilities is deprecated. Use the data module instead",
    DeprecationWarning,
    stacklevel=2,
)
