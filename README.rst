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

But if you simiply need to something simple: check whether a point is in a polygon, it's nice to have a simple set of functions to do the basic stuff on numpy arrays, without all the overhead of a full set of geometry objects.

Features
========

This is a start, but it will likely never be very comprehensive.

polygons
--------

polygons are represented by a Nx2 numpy array of floats. (or somethign that can be turned into one):

``polygon_inside``
..................

Determine if points are inside a polygon.







