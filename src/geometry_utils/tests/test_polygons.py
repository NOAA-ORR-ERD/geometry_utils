"""
test code for the polygons.py API
"""

from pathlib import Path

import numpy as np
import pytest

from geometry_utils import (polygon_inside,
                            polygon_rotation,
                            polygon_area,
                            polygon_centroid,
                            polygon_is_simple,
                            )
# from geometry_utils.cy_polygons import polygon_centroid

try:
    import matplotlib.pyplot as plt
    HAVE_MPL = True
    OUTPUT_DIR = Path(__file__).parent / "plots"
    OUTPUT_DIR.mkdir(exist_ok=True)
except ImportError:
    HAVE_MPL = False


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

polys = [([(5, 5), (5, 15), (15, 15), (15, 5)], (10, 10), 'square'), # simple square
         ([(2, 7), (6, 3), (2, 4)], [3.33333333, 4.66666667], 'triangle'), # triangle
         ([[-2., -7.], [-6., -3.], [-2., -4.]], [-3.33333333, -4.66666667], "triangle_2"),  # same in negative coords
         ([(-100, 0), (0, -100), (100, 0), (0, 100)], (0.0, 0.0), "diamond"),  # diamond around origin
         # more complicated, with the centroid outside the polygon looks right, so preserved the result
         ([(-700, 1000), (800, 1010), (1200, 200), (500, 900), (-600, 890), (-1300, -20)], (126.43211, 781.0239), 'outside'),
         ]

@pytest.mark.parametrize(('poly', 'result', 'name'), polys)
def test_polygon_centroid(poly, result, name):

    centroid = polygon_centroid(poly)
    print(f"{poly=}")
    print(f"{centroid=}")

    # duplicate the end point -- should be the same
    poly.append(poly[0])
    # plot before the assert, in case it fails
    if HAVE_MPL:
        poly = np.asarray(poly)
        fig, ax = plt.subplots()
        ax.plot(poly[:, 0], poly[:, 1], '-o')
        ax.plot(centroid[0], centroid[1], 'ro')
        fig.savefig(OUTPUT_DIR / f"centroid_{name}.png")

    assert np.allclose(centroid, result)

    centroid = polygon_centroid(poly)
    print(f"{poly=}")
    print(f"{centroid=}")
    assert np.allclose(centroid, result)

simple_polys = [
               ([(5, 5), (5, 15), (15, 15), (15, 5)], 'square'), # simple square
               ([[-2., -7.], [-6., -3.], [-2., -4.]],  "triangle"),  # same in negative coords
               ([(-100, 0), (0, -100), (100, 0), (0, 100)], "diamond"),  # diamond around origin
               # more complicated, with the centroid outside the polygon looks right, so preserved the result
               ([(-700, 1000), (800, 1010), (1200, 200), (500, 900), (-600, 890), (-1300, -20)], 'complex'),
                ]

@pytest.mark.parametrize(('poly', 'name'), simple_polys)
def test_polygon_is_simple_yes(poly, name):
    """
    tests simple polygons
    """
    if HAVE_MPL:
        plot_poly(poly, OUTPUT_DIR / f"not_intersecting_{name}.png")

    assert polygon_is_simple(poly)

#    assert False

intersecting_polys = [
               # ([(5, 5), (15, 15), (5, 15),  (15, 5)], 'AnX'), # simple square
               ([[-2., -7.], [-6., -3.], [-2., -7.]],  "zero_area_triangle"),  # triangle can only be bad if points repeat.
               # ([(0, -100), (-100, 0), (100, 0), (0, 100)], "diamond"),  # diamond around origin
               # # # more complicated, with the centroid outside the polygon looks right, so preserved the result
               # ([(-700, 1000), (800, 1010), (1200, 200), (1100, 900), (-600, 890), (-1300, -20)], 'complex'),
               # # duplicated point
               # ([(5, 5), (5, 15), (5, 15), (15, 15), (15, 5)], "duplicated_point"),
                ]

@pytest.mark.parametrize(('poly', 'name'), intersecting_polys)
def test_polygon_is_simple_no(poly, name):
    """
    tests simple polygons
    """
    if HAVE_MPL:
        plot_poly(poly, OUTPUT_DIR / f"intersecting_{name}.png")

    assert not polygon_is_simple(poly)
    # assert False

# plotting utility
def plot_poly(poly, filename):
    poly = np.asarray(poly)
    fig, ax = plt.subplots()
    ax.plot(poly[:, 0], poly[:, 1], '-o')
    ax.plot([poly[-1, 0], poly[0, 0]], [poly[-1, 1], poly[0, 1]], 'r-')
    fig.savefig(filename)
