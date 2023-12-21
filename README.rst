##############
geometry_utils
##############

.. image:: https://img.shields.io/travis/ChrisBarker-NOAA/geometry_utils.svg
        :target: https://travis-ci.org/ChrisBarker-NOAA/geometry_utils
.. image:: https://circleci.com/gh/ChrisBarker-NOAA/geometry_utils.svg?style=svg
    :target: https://circleci.com/gh/ChrisBarker-NOAA/geometry_utils
.. image:: https://codecov.io/gh/ChrisBarker-NOAA/geometry_utils/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ChrisBarker-NOAA/geometry_utils


Utilities for basic computational geometry directly with numpy arrays.

Motivation
==========

There are a number of copmutational geometry libraries available.
But most of them create a whole framework of objects: points, polygons,
MultiPolygons, etc.

But if you simply need to something simple: e.g. check whether a point is in a polygon, it's nice to have a simple set of functions to do the basic stuff on numpy arrays, without all the overhead of a full set of geometry objects.

These functions all depend on numpy. Some of the functons a pure (numpy) python, and some are written in Cython, or C wrapped in Cython. Most are vectorized, for fast results. e.g. points_in_polygon will check whether multiple points are in a polygon all in C.

Features
========

This is a start, but it will likely never be very comprehensive.

NOTE: this is all 2D euclidean geometry

Data Structures
---------------

The goal is not to have specialized data structures, but to use "normal" numpy arrays (usually float64) to represent geometrical objects.

Most functions will (like numpy itself) take standard Python data structures (such as lists) and convert to numpy arrays as needed (`np.asarray()`).

points
......

Points are represented by a shape: ``(2,)`` array (or 2-tuple):
``(x, y)`` of type ``float64``


Multiple points
...............

Multiple points are represented by a shape: ``(N,2)`` array: ``[(x, y), )x,y),...]`` of type ``float64`` (or equivalent nested list).


Polygons
........

Multiple points are represented by a shape: ``(N,2)`` array: ``[(x, y), )x,y),...]`` of type ``float64`` (or equivalent nested list).
(Note that this is exactly the same as multipel points)

Functions
---------

``polygon_inside``
..................

Determine if points are inside a polygon.







