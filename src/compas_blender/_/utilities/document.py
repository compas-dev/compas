import os


__author__     = ['Andrew Liew  <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Andrew Liew'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


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
