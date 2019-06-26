
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass

import os


__all__ = [
    'get_document_name',
    'get_document_filename',
    'get_document_path',
    'get_document_dirname'
]


def get_document_name():
    raise NotImplementedError


def get_document_filename():
    raise NotImplementedError


def get_document_path():
    raise NotImplementedError


def get_document_dirname():
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
