from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

from compas.data.coercion import coerce_sequence_of_list  # noqa: F401
from compas.data.coercion import coerce_sequence_of_tuple  # noqa: F401
from compas.data.validators import is_sequence_of_str  # noqa: F401
from compas.data.validators import is_sequence_of_int  # noqa: F401
from compas.data.validators import is_sequence_of_float  # noqa: F401
from compas.data.validators import is_sequence_of_tuple  # noqa: F401
from compas.data.validators import is_sequence_of_list  # noqa: F401
from compas.data.validators import is_sequence_of_dict  # noqa: F401
from compas.data.validators import is_sequence_of_iterable  # noqa: F401
from compas.data.validators import is_item_iterable  # noqa: F401


warnings.warn(
    "The coercing module in utilities is deprecated. Use the data module instead",
    DeprecationWarning,
    stacklevel=2,
)
