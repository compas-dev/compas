import os

try:
    import rhinoscriptsyntax as rs

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'get_document_name',
    'get_document_filename',
    'get_document_path',
    'get_document_dirname'
]


def get_document_name():
    return rs.DocumentName()


def get_document_filename():
    return os.path.splitext(get_document_name())[0]


def get_document_path():
    return rs.DocumentPath()


def get_document_dirname():
    return os.path.dirname(get_document_path())


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
