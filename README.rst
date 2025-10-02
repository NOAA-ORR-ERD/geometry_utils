##############
geometry_utils
##############

Utilities for basic computational geometry directly with numpy arrays.


Motivation
==========

There are a number of computational geometry libraries available.
But most of them create a whole framework of objects: Points, Polygons,
MultiPolygons, etc.

But if you simply need to something simple, e.g. to check whether a point is in a polygon,
it's nice to have a set of functions to do the basic stuff on numpy arrays,
without all the overhead of a full set of geometry objects.

These functions all depend on numpy.

Some of the functions a pure (numpy) python, and some are written in Cython, or C wrapped in Cython.

Most are vectorized, for fast results. e.g. ``polygon_inside`` will check whether multiple points are in a single polygon all in compiled code.

Features
========

This is a start, and it will likely never be very comprehensive, but there are useful utilities here.

NOTE: this is all 2D euclidean geometry

* Basic polygon manipulation

* Some rectangle (bounding box) functionality


Data Structures
---------------

The goal is to not have specialized data structures, but to use "normal" numpy arrays (usually with dtype ``float64``) to represent geometrical objects.

Most functions will (like numpy itself) take standard Python data structures (such as lists) and convert to numpy arrays as needed (``np.asarray()``).

Points
......

Points are represented by a shape: ``(2,)`` array (or 2-tuple):
``(x, y)`` of type ``float64``


Multiple points
...............

Multiple points are represented by a shape: ``(N, 2)`` array:
``[(x, y), (x, y), ...]`` of type ``float64`` (or equivalent nested list).


Polygons
........

Polygons are represented by their vertixes as a shape: ``(N,2)`` array:
``[(x, y), (x, y), ...]`` of type ``float64``
(or equivalent nested list).

(Note that this is exactly the same as multiple points)

Rectangles
..........

Rectangles are axis-aligned rectangles -- suitable for use as bounding boxes, etc.

A rectangle is defined by two points: lower-left, upper-right.

Any python sequence that can be turned into a 2x2 numpy array of float64s::

    [[min_x, min_y],
     [max_x, max_y]]


Functions
---------

``polygon_inside(polygon_verts, trial_points)``
...............................................

Determine if points are inside a polygon.

``polygon_area(polygon_verts)``
...............................

Calculate the area of a polygon


``polygon_rotation(polygon_verts)``
...................................

Returns an int/bool flag indicating the "winding order" of the polygon

i.e. clockwise or anti-clockwise

``polygon_centroid(polygon_verts)``
...................................

Return the (x, y) location of the polygon centroid


``polygon_is_simple(polygon_verts)``
....................................

checks whether the polygon is simple, i.e. has any segments that cross each other.

Development
===========

This code includes Cython code -- so to work on it, you need Cython and a compiler set up to compile Python extensions. Consult the internet to see how to do that.

Once your compiler is set up and dependencies in place:

``pip install .``

Should build and install the package.

Note that if you do an editable install:

``pip isntall -e .``

The python code will be editable, but you need to rebuild if you change the Cython code.

conda
-----

All the dependencies to build and use this package are available on conda-forge.

pixi
----

This package includes a pixi setup to aid in development and building -- see the ``pixi.toml`` file.

https://pixi.sh/latest/

To use:

``pixi run shell``

Will get you a pixi shell with the dependencies installed, but not the package. You can then pip install the package.

This is helpful if you are working on the Cython code, so that you can control the install


``pixi run -e dev shell``


Will create a pixi shell with the package built and installed. You can then run the tests, change the  code, etc.

``pixi run build``

Will build and install the package.

``pixi run test``

Will build, and test the package.

``pixi run -e py310 test``

will build and test the package with python 3.10

``py311``, ``py312``, ``py313`` are also available.
