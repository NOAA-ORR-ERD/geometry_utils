from setuptools import setup
import versioneer
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

cmdclass = versioneer.get_cmdclass()
cmdclass['build_ext'] = build_ext

setup(
    name='geometry_utils',
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    description="Utilities for basic computational geometry directly with numpy arrays.",
    author="Christopher Barker, Rob Hetland",
    author_email='Chris.Barker@noaa.gov',
    url='https://github.com/NOAA-ORR-ERD/geometry_utils',
    packages=['geometry_utils'],
    ext_modules=ext_modules,
    install_requires=requirements,
    keywords='geometry_utils',
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
