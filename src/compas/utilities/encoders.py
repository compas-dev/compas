from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

from compas.data import DataEncoder
from compas.data import DataDecoder

__all__ = ["DataEncoder", "DataDecoder"]

warnings.warn(
    "The encoders module in utilities is deprecated. Use the encoders module from data instead",
    DeprecationWarning,
    stacklevel=2,
)
