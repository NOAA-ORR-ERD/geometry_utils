from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy  # for the includes for the Cython code

# package requirements go here
requirements = ["numpy",
                ]

ext_modules = [Extension("geometry_utils.cy_polygons",
                         sources=["geometry_utils/cy_polygons.pyx",
                                  "geometry_utils/c_point_in_polygon.c"],
                         include_dirs=[numpy.get_include()]),
               Extension("geometry_utils.cy_line_crossings",
                         sources=["geometry_utils/cy_line_crossings.pyx"],
                         include_dirs=[numpy.get_include()]),
               ]

# cmdclass = versioneer.get_cmdclass()
# cmdclass['build_ext'] = build_ext

setup(
    ext_modules=ext_modules,
)
