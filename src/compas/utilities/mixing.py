from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'mix_in_functions',
    'mix_in_class_attributes',
]


# @see: http://code.activestate.com/recipes/577824-mixins-by-inheritance-vs-by-decoratorlets-try-deco/
# @see: http://scottlobdell.me/2015/04/decorators-arguments-python/
# @see: http://duganchen.ca/implementing-pythonic-mixins-with-class-decorators/
# @see: https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc


def mix_in_functions(mixins, overwrite=False):
    def decorate(cls):
        # attr = {}
        for func in mixins:
            if not overwrite:
                if hasattr(cls, func.__name__):
                    continue
            # attr[func.__name__] = func
            setattr(cls, func.__name__, func)
        # cls = type(cls.__name__, (cls, ), attr)
        return cls
    return decorate


def mix_in_class_attributes(mixins, overwrite=False, protected=False):
    def decorate(cls):
        # attr = {}
        for mixin in mixins:
            for name, value in mixin.__dict__.items():
                # magic methods
                if name.startswith('__') and name.endswith('__'):
                    continue
                # protected / private methods
                if not protected and name.startswith('_'):
                    continue
                # existing methods
                if not overwrite:
                    if hasattr(cls, name):
                        continue
                # attr[name] = value
                setattr(cls, name, value)
        # cls = type(cls.__name__, (cls, ), attr)
        return cls
    return decorate


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import inspect

    # test3
    def func1(self):
        print('f1')

    def func2(self):
        print('f2')

    class B(object):
        """"""

        def func1(self):
            print('B')

        # test4
        def meth1(self):
            print('B')

        def _meth(self):
            print('B')

    @mix_in_class_attributes((B, ), protected=True, overwrite=False)
    @mix_in_functions((func1, func2))
    # test1
    # test2
    class A(object):
        pass

    print('mro', inspect.getmro(A))
    print('comments', inspect.getcomments(A.func1))
    print('comments', inspect.getcomments(A.meth1))
    print('dir', dir(A))

    a = A()
    a.func1()
    a.func2()
    a.meth1()
    a._meth()
