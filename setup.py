# from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Build import cythonize

# extensions = [
#     Extension(
#         "compas.geometry.hpc.cpoint",
#         sources=["compas/geometry/hpc/cpoint.pyx"]
#         # language="c++"
#     ),
#     Extension(
#         "compas.geometry.hpc.cvector",
#         sources=["compas/geometry/hpc/cvector.pyx"]
#         # language="c++"
#     ),
# ]

# setup(
#     ext_modules=cythonize(extensions)
# )

from setuptools import setup
from setuptools import find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='compas',
    version='0.1.0',
    description='The COMPAS framework',
    long_description=long_description,
    license='MIT',
    url='http://compas-dev.github.io',
    author='Tom Van Mele',
    author_email='van.mele@arch.ethz.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='architecture fabrication engineering',
    packages=find_packages('src', exclude=['compas_rhino', 'compas_maya', 'compas_blender']),
    package_dir={'': 'src'},
    package_data={'compas': ['*.dll', '*.so']},
    # include_package_data=True,  # combine with MANIFEST.in
    # exclude_package_data={},
    data_files=[('', ['LICENSE', 'README.md']), ('samples', ['*.obj', '*.json'])],
    install_requires=[],
    python_requires='>=2.7',
    # py_modules=[],
    # entry_points={},
)
