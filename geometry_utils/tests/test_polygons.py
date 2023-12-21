"""
test code for the polygons.py API
"""

import numpy as np
import pytest

from geometry_utils import (polygon_inside,
                            polygon_rotation,
                            polygon_area,
                            )

# Example data

poly1 = [(3.0, 3.0),
         (5.0, 8.0),
         (10.0, 5.0),
         (7.0, 1.0),
         ]

pt1 = (3.0, 6.0)  # outside
pt2 = (6.0, 4.0)  # inside
pt3 = (9.0, 7.0)  # outside

poly1_ccw = np.array((
    (-5, -2),
    (3, -1),
    (5, -1),
    (5, 4),
    (3, 0),
    (0, 0),
    (-2, 2),
    (-5, 2),
    ), dtype=np.float64)

poly1_cw = poly1_ccw[::-1].copy()


def test_polygon_inside_single_point():
    result = polygon_inside(poly1, pt1)

    assert result is False


def test_polygon_inside_multiple_points():
    result = polygon_inside(poly1, [pt1, pt2, pt3])

    print(result)

    assert np.all(result == [False, True, False])


def test_rotation_cw():
    assert polygon_rotation(poly1_cw) == 1


def test_rotation_ccw():
    assert polygon_rotation(poly1_ccw) == 0


def test_rotation_zero_area():
    poly = [(5.0, 5.0), (1.0, 3.1), (5.0, 5.0)]
    with pytest.raises(ValueError):
        polygon_rotation(poly)


poly_areas = [([(0, 0), (0, 2.0), (4.0, 2.0), (4.0, 0.0)], 8.0),  # rectangle
              ([(0, 0), (0, 2.0), (4.0, 2.0), (4.0, 0.0), (0, 0)], 8.0),  # duplicated end point
              ([(4, 0), (4, 2.0), (0.0, 2.0), (0.0, 0.0)], 8.0),  # rectangle
              ([(2, 2), (4, 10), (6, 2)], 16.0),  #  triangle
              ([(2, 2), (4, 10), (6, 2), (2, 2)], 16.0),  #  triangle
              ]


@pytest.mark.parametrize(('poly', 'area'), poly_areas)
def test_polygon_area(poly, area):
    assert polygon_area(poly) == area



