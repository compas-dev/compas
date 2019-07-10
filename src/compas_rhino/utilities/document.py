from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'get_document_basename',
    'get_document_filename',
    'get_document_extension',
    'get_document_filepath',
    'get_document_dirname'
]


def get_document_basename():
    return rs.DocumentName()


def get_document_filename():
    basename = get_document_basename()
    if not basename:
        return None
    return os.path.splitext(basename)[0]


def get_document_extension():
    basename = get_document_basename()
    if not basename:
        return None
    return os.path.splitext(basename)[1]


def get_document_filepath():
    return rs.DocumentPath()


def get_document_dirname():
    filepath = get_document_filepath()
    if not filepath:
        return None
    return os.path.dirname(filepath)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
