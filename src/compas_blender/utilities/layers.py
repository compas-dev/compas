
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'create_layers_from_path',
    'create_layers_from_paths',
    'create_layers_from_dict',
    'create_layers',
    'clear_layer',
    'clear_current_layer',
    'clear_layers',
    'delete_layers',
]


# ==============================================================================
# helpers
# ==============================================================================

def show_hidden_objects_on_layer(name):

    raise NotImplementedError


def find_objects_on_layer(name, include_hidden=True, include_children=True):

    raise NotImplementedError


def delete_objects_on_layer(name, include_hidden=True, include_children=False, purge=True):

    raise NotImplementedError


# ==============================================================================
# create
# ==============================================================================

def create_layers_from_path(path, separator='::'):

    raise NotImplementedError


def create_layers_from_paths(names, separator='::'):

    raise NotImplementedError


def create_layers_from_dict(layers):

    raise NotImplementedError


create_layers = create_layers_from_dict


# ==============================================================================
# clear
# ==============================================================================

def clear_layer(name, include_hidden=True, include_children=True, purge=True):

    raise NotImplementedError


def clear_current_layer():

    raise NotImplementedError


def clear_layers(layers, include_children=True, include_hidden=True):

    raise NotImplementedError


# ==============================================================================
# delete
# ==============================================================================

def delete_layers(layers):

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
