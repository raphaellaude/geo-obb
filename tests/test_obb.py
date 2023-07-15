import geopandas as gpd
from shapely.geometry import Polygon, LineString
from geoobb.obb import *
from numpy.testing import assert_array_almost_equal
from pandas import Series


SQUARE = Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)))
RECTANGLE = Polygon(((0, 0), (2, 0), (2, 1), (0, 1), (0, 0)))
LOSANGE = Polygon(((0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5), (0.5, 0.5)))
TRIANGLE = Polygon(((0, 0), (1, 0), (0, 1), (0, 0)))
LINE = LineString(((0, 0), (1, 1)))


def test_geom_to_unique_array():
    """
    Tests the geometry to array conversion.
    """
    geometry = gpd.GeoSeries((SQUARE, RECTANGLE, LOSANGE, TRIANGLE, LINE))
    arrays: Series = geometry.map(geom_to_unique_array)
    assert_array_almost_equal(arrays[0], [[0, 0], [0, 1], [1, 0], [1, 1]])
    assert_array_almost_equal(arrays[1], [[0, 0], [0, 1], [2, 0], [2, 1]])
    assert_array_almost_equal(arrays[2], [[0.5, 0.5], [0.5, 1.5], [1.5, 0.5], [1.5, 1.5]])
    assert_array_almost_equal(arrays[3], [[0, 0], [0, 1], [1, 0]])
    assert_array_almost_equal(arrays[4], [[0, 0], [1, 1]])


def test_oriented_bounding_box():
    """
    Tests the oriented bounding box calculation.
    """
    geometry = gpd.GeoSeries((SQUARE, RECTANGLE, LOSANGE, TRIANGLE, LINE))
    oobs = geometry.map(geom_to_unique_array).map(oriented_bounding_box_dimensions)
    assert_array_almost_equal(oobs[0], [1, 1])
    assert_array_almost_equal(oobs[1], [2, 1])
    assert_array_almost_equal(oobs[2], [1, 1])
    assert_array_almost_equal(oobs[3], [1.5, 0.5])
    assert_array_almost_equal(oobs[4], [1, 1])
