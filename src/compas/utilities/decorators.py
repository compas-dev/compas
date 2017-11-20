import abc


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def add_metaclass(metaclass):
    pass


class abstractstatic(staticmethod):
    __slots__ = []

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":

    class A(object):
        __metaclass__ = abc.ABCMeta

        @abstractstatic
        def test():
            pass

    class B(A):

        @staticmethod
        def test():
            print(B.__metaclass__)

    b = B()

    b.test()
