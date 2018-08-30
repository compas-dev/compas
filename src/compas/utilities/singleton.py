from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


class Singleton(object):

    __instance = None

    def __new__(cls):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        return Singleton.__instance


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    a = Singleton()

    for i in range(10):
        b = Singleton()

        print(a is b)
