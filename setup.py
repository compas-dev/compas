#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function

import io
from os import path

from setuptools import find_packages, setup

requirements = []
optional_requirements = {}

here = path.abspath(path.dirname(__file__))

def read(*names, **kwargs):
    return io.open(
        path.join(here, *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

long_description = read('README.md')

setup(
    name='COMPAS',
    version='0.2.4',
    description='The COMPAS framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://compas-dev.github.io',
    author='Tom Van Mele',
    author_email='van.mele@arch.ethz.ch',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords=['architecture', 'fabrication', 'engineering'],
    project_urls={
        "Documentation": "http://compas-dev.github.io",
        "Forum": "https://forum.compas-framework.org/",
        "Repository": "https://github.com/compas-dev/compas",
        "Issues": "https://github.com/compas-dev/compas/issues",
    },

    packages=['compas', 'compas_rhino', 'compas_blender', 'compas_ghpython', ],
    package_dir={'': 'src'},
    package_data={
        '': ['_data/*.obj']
    },
    data_files=[
    ],
    include_package_data=True,

    zip_safe=False,

    install_requires=requirements,
    python_requires='>=2.7',
    extras_require=optional_requirements,

    entry_points={
        'console_scripts': [],
    },

    ext_modules=[]
)
