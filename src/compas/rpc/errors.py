from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['RPCServerError', 'RPCClientError']


class RPCServerError(Exception):
    pass


class RPCClientError(Exception):
    pass
