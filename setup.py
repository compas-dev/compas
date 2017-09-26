from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "compas.geometry.hpc.cpoint",
        sources=["compas/geometry/hpc/cpoint.pyx"]
        # language="c++"
    ),
    Extension(
        "compas.geometry.hpc.cvector",
        sources=["compas/geometry/hpc/cvector.pyx"]
        # language="c++"
    ),
]

setup(
    ext_modules=cythonize(extensions)
)
