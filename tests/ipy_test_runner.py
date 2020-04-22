# This is a very simple replacement for pytest on IronPython
# Only the absolutely minimal features we need are supported
# It makes a ton of assumptions. Deal with it.
from __future__ import print_function

import argparse
import contextlib
import fnmatch
import functools
import imp
import os
import random
import sys
import time
import traceback
import types
from StringIO import StringIO

FIXTURES = dict()


@contextlib.contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def discover_tests(directory, pattern):
    for root, _dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def print_title(title, sep='='):
    size = int((80 - len(title)) / 2)
    print(sep * size, title, sep * size)


def load_fake_module(name, fake_types=None, stubs=None):
    module = types.ModuleType(name)
    types_dict = dict()
    if fake_types:
        for type_name in fake_types:
            types_dict[type_name] = type(type_name, (object,), dict(__module__=module))
    if stubs:
        for stub_key, stub_type in stubs.items():
            types_dict[stub_key] = stub_type
    module.__dict__.update(types_dict)
    sys.modules[name] = module


def fixture(func):
    FIXTURES[func.__name__] = func
    return func


def parametrize(argnames='', argvalues=None):
    def decorator_param(func):
        func._parametrized_arguments = dict(argnames=argnames, argvalues=argvalues)
        return func

    return decorator_param


@contextlib.contextmanager
def raises(exception_type):
    did_raise = False
    try:
        yield []
    except Exception as e:
        if isinstance(e, exception_type):
            did_raise = True
    finally:
        if not did_raise:
            raise AssertionError('Did not raise exception of type {}'.format(exception_type))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IronPython pytest runner.')
    parser.add_argument('--test-dir', type=str, help='Test directory', default=os.path.dirname(__file__))
    parser.add_argument('--exclude', type=str, action='append',
                        help='Test files to exclude')

    args = parser.parse_args()
    pattern = 'test_*.py'

    load_fake_module('pytest', stubs=dict(fixture=fixture, raises=raises, mark=argparse.Namespace(parametrize=parametrize)))

    # Fake Rhino modules
    load_fake_module('Rhino')
    load_fake_module('Rhino.Geometry', fake_types=['RTree', 'Sphere', 'Point3d'])

    loaded_modules = list(sys.modules)

    counter = 0
    errors = 0
    collected_errors = dict()

    start_time = time.time()
    print_title('test session starts')

    for test_module in discover_tests(args.test_dir, pattern):
        if args.exclude:
            if test_module in args.exclude:
                print('Skipping {} module'.format(test_module))
                continue

        print(test_module, end=' ')
        module = imp.load_source('{}_{}'.format(test_module, counter), test_module)
        test_methods = [fname for fname in dir(module) if fname.startswith('test_')]
        random.shuffle(test_methods)

        for test_method_name in test_methods:
            test_method = getattr(module, test_method_name)

            # Build argument sets
            parametrized_arguments = []
            if hasattr(test_method, '_parametrized_arguments'):
                argnames = test_method._parametrized_arguments['argnames']
                argnames = argnames.split(',') if isinstance(argnames, str) else argnames
                for argvalues in test_method._parametrized_arguments['argvalues']:
                    partial_args = dict()
                    # Special handling for just on argument
                    if len(argnames) == 1:
                        partial_args[argnames[0]] = argvalues
                    else:
                        partial_args = {k: v for k, v in zip(argnames, argvalues)}
                    parametrized_arguments.append(partial_args)
            else:
                # Default invocation without arguments
                parametrized_arguments = [dict()]

            parametrize_counter = 0
            for kwargs in parametrized_arguments:
                counter += 1
                parametrize_counter += 1

                # Invoke test
                result = dict(test_module=test_module, test_method=test_method_name)

                with capture() as out:
                    try:
                        argument_names = test_method.__code__.co_varnames[0:test_method.__code__.co_argcount]

                        # Inject fixture if needed
                        for argkey in argument_names:
                            if argkey in kwargs:
                                continue
                            if argkey not in FIXTURES:
                                raise Exception('Test method "{}" needs argument "{}" but no fixture with that name'.format(test_method_name, argkey))
                            kwargs[argkey] = FIXTURES[argkey]()

                        # Invoke test method
                        test_method(**kwargs)

                        result['result'] = '.'
                    except:
                        errors += 1
                        result['result'] = 'F'
                        result['exception'] = traceback.format_exc()
                        result['exception_message'] = sys.exc_info()[1]
                    finally:
                        result['out'] = out
                        # Unload modules loaded by the test
                        modules_loaded_by_test = [m for m in sys.modules if m not in loaded_modules]
                        for module_to_unload in modules_loaded_by_test:
                            sys.modules.pop(module_to_unload)

                print(result['result'], end='')
                if result['result'] == 'F':
                    key = '{}::{}[{}]'.format(test_module, test_method_name, parametrize_counter)
                    collected_errors[key] = result

        print()

    end_time = time.time()

    if errors > 0:
        print()
        print_title('FAILURES')
        for key, result in collected_errors.items():
            print_title(key, sep='_')
            print(result['exception'])
            needs_title = True
            for o in result['out']:
                if len(o):
                    if needs_title:
                        print_title('Captured stdout', sep='-')
                        needs_title = False
                    print(o)

        print_title('short test summary info')
        for key, result in collected_errors.items():
            print('FAILED {} - {}'.format(key, result['exception_message']))

    print_title('{} failed, {} passed in {:.2f}s'.format(errors, counter - errors, end_time - start_time))
    sys.exit(errors)
