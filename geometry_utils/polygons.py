#!/usr/bin/env python

"""
Single module to hold the high-level API for working with polygons
"""

import numpy as np

from .cy_polygons import (points_in_poly,
                                  points_in_polys,
                                  signed_area,
                                  )
from . import cy_polygons as cyp


def polygon_inside(polygon_verts, trial_points):
    '''
    Return a Boolean array the size of the trial point array True if point is inside

    INPUTS
    ------
    polygon_verts:  Mx2 array
    trial_points:   Nx2 array

    RETURNS
    -------
    inside_points:  Boolean array (len(N))
                    True if the trial point is inside the polygon
    '''

    polygon_verts = np.asarray(polygon_verts, dtype=np.float64)
    trial_points = np.asarray(trial_points, dtype=np.float64)
    return points_in_poly(polygon_verts, trial_points)


def polygon_area(polygon_verts):
    """
    Calculate the area of a polygon

    expects a sequence of tuples, or something like it (Nx2 array for instance),
    of the points:

    [ (x1, y1), (x2, y2), (x3, y3), ...(xi, yi) ]

    It simply computes the signed area -- the sign is CW or CCW
    See: http://paulbourke.net/geometry/clockwise/
    """

    polygon_verts = np.asarray(polygon_verts, np.float64)
    return abs(signed_area(polygon_verts))


def polygon_is_simple(polygon_verts):
    '''
    Return true if the polygon is simple

    i.e. has no crossing segments, etc.
    '''

    # code
    raise NotImplementedError

    # return issimple


def polygon_rotation(polygon_verts, convex=False):
    '''
    Return a int/bool flag indicating the "winding order" of the polygon

    i.e. clockwise or anti-clockwise

    INPUT
    -----
    polygon_verts:  Mx2 array

    convex=False: flag to indicate if the polygon is convex
                  -- if it is convex, a faster algorithm will be used.

    OUTPUT
    ------
    rotation:  scalar / boolean
               1 for a positive rotation according to the right-hand rule
               0 for a negative rotation according to the right hand rule

               Note, only defined for a simple polygon. Behavior is undetermined
               if the polygon has holes or crossing segments.

    '''
    # fixme: need a test for a simple polygon!

    polygon_verts = np.asarray(polygon_verts, np.float64)
    s_a = signed_area(polygon_verts)
    if s_a < 0:
        return 1
    elif s_a > 0:
        return 0
    else:
        raise ValueError("can't compute rotation of a zero-area polygon")


def polygon_centroid(polygon_verts):
    """
    Return the (x, y) location of the polygon centroid

    This is the "center of gravity" centroid -- it will not necessarily
    fall inside the polygon for convex polygons.

    INPUT
    -----
    polygon_verts:  Nx2 array

    OUTPUT
    ------
    xy_centroid:  (2,)

    NOTE: possible implimentation:
    https://lexrent.eu/wp-content/uploads/torza/artikel_groep_sub_2_docs/BYZ_3_Polygon-Area-and-Centroid.pdf
    or
    https://en.wikipedia.org/wiki/Centroid#Of_a_polygon

    """
    # from:

    # https://stackoverflow.com/questions/2792443/finding-the-centroid-of-a-polygon

    # Here is Emile Cormier's algorithm without duplicated code or
    # expensive modulus operations, best of both worlds:

    # #include <iostream>

    # using namespace std;

    # struct Point2D
    # {
    #     double x;
    #     double y;
    # };

    # Point2D compute2DPolygonCentroid(const Point2D* vertices, int vertexCount)
    # {
    #     Point2D centroid = {0, 0};
    #     double signedArea = 0.0;
    #     double x0 = 0.0; // Current vertex X
    #     double y0 = 0.0; // Current vertex Y
    #     double x1 = 0.0; // Next vertex X
    #     double y1 = 0.0; // Next vertex Y
    #     double a = 0.0;  // Partial signed area

    #     int lastdex = vertexCount-1;
    #     const Point2D* prev = &(vertices[lastdex]);
    #     const Point2D* next;

    #     // For all vertices in a loop
    #     for (int i=0; i<vertexCount; ++i)
    #     {
    #         next = &(vertices[i]);
    #         x0 = prev->x;
    #         y0 = prev->y;
    #         x1 = next->x;
    #         y1 = next->y;
    #         a = x0*y1 - x1*y0;
    #         signedArea += a;
    #         centroid.x += (x0 + x1)*a;
    #         centroid.y += (y0 + y1)*a;
    #         prev = next;
    #     }

    #     signedArea *= 0.5;
    #     centroid.x /= (6.0*signedArea);
    #     centroid.y /= (6.0*signedArea);

    #     return centroid;
    # }

    # int main()
    # {
    #     Point2D polygon[] = {{0.0,0.0}, {0.0,10.0}, {10.0,10.0}, {10.0,0.0}};
    #     size_t vertexCount = sizeof(polygon) / sizeof(polygon[0]);
    #     Point2D centroid = compute2DPolygonCentroid(polygon, vertexCount);
    #     std::cout << "Centroid is (" << centroid.x << ", " << centroid.y << ")\n";
    # }

    # this is computing the area and the centroids of each area segment at the same time
    # so it is the same code as the area, with a bit of extra

    polygon_verts = np.asarray(polygon_verts, np.float64)
    return cyp.polygon_centroid(polygon_verts)

    # # python version -- not very different
    # nvert = polygon_verts.shape[0]
    # x = 0.0
    # y = 0.0

    # area = ((polygon_verts[nvert - 1, 0] * polygon_verts[0, 1]) -
    #          (polygon_verts[0, 0] * polygon_verts[nvert - 1, 1])
    #          )  # last point to first point
    # x += (polygon_verts[nvert - 1, 0] + polygon_verts[0, 0]) * area
    # y += (polygon_verts[nvert - 1, 1] + polygon_verts[0, 1]) * area

    # for i in range(nvert - 1):
    #     a = ((polygon_verts[i, 0] * polygon_verts[i + 1, 1]) -
    #               (polygon_verts[i + 1, 0] * polygon_verts[i, 1])
    #               )
    #     area += a
    #     x += (polygon_verts[i, 0] + polygon_verts[i + 1, 0]) * a
    #     y += (polygon_verts[i, 1] + polygon_verts[i + 1, 1]) * a

    # area /= 2.0
    # x /= (6.0 * area)
    # y /= (6.0 * area)

    # return (x, y)



