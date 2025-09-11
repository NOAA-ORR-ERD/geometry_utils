#!/usr/bin/env python

"""
Test code for core types
"""

import numpy as np
import pytest

from geometry_utils.utilities import point
from geometry_utils.cy_core_types import Point, Vector, Interval, Box, Triangle

def test_point():
    pt = Point(3, 4)

    assert pt.x == 3.0
    assert pt.y == 4.0

    with pytest.raises(TypeError):
        pt = Point(3, "barney")

def test_point_index():
    pt = Point(3, 4)

    assert pt[0] == 3.0
    assert pt[1] == 4.0

    with pytest.raises(IndexError):
        pt[2]


def test_vector():
    vc = Vector(3, 4)

    assert vc.x == 3.0
    assert vc.y == 4.0

    with pytest.raises(TypeError):
        pt = Vector(3, "barney")

# The following tests only test that they can be instantiated

def test_interval():
    Interval(3, 4)

def test_box():
    Box(1, 2, 3, 4)

def test_triangle():
    Triangle(Point(1, 2), b=Point(3, 4), c=Point(5, 6))

