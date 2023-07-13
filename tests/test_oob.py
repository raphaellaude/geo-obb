import geopandas as gpd
from shapely.geometry import Polygon, LineString
from geooob.oob import geom_to_array, oriented_bounding_box
from numpy.testing import assert_array_almost_equal
from pandas import Series


SQUARE = Polygon(((0, 0), (1, 0), (1, 1), (0, 1), (0, 0)))
RECTANGLE = Polygon(((0, 0), (2, 0), (2, 1), (0, 1), (0, 0)))
LOSANGE = Polygon(((0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5), (0.5, 0.5)))
TRIANGLE = Polygon(((0, 0), (1, 0), (0, 1), (0, 0)))
LINE = LineString(((0, 0), (1, 1)))


def test_geom_to_array():
    geometry = gpd.GeoSeries((SQUARE, RECTANGLE, LOSANGE, TRIANGLE, LINE))
    arrays: Series = geometry.map(geom_to_array)
    assert_array_almost_equal(arrays[0], [[0, 0], [0, 1], [1, 0], [1, 1]])
    assert_array_almost_equal(arrays[1], [[0, 0], [0, 1], [2, 0], [2, 1]])
    assert_array_almost_equal(arrays[2], [[0.5, 0.5], [0.5, 1.5], [1.5, 0.5], [1.5, 1.5]])
    assert_array_almost_equal(arrays[3], [[0, 0], [0, 1], [1, 0]])
    assert_array_almost_equal(arrays[4], [[0, 0], [1, 1]])


def test_oriented_bounding_box():
    geometry = gpd.GeoSeries((SQUARE, RECTANGLE, LOSANGE, TRIANGLE, LINE))
    oobs: Series[Polygon] = geometry.map(geom_to_array).map(oriented_bounding_box).map(Polygon)
    assert_array_almost_equal(oobs[0].area, 1)
    assert_array_almost_equal(oobs[1].area, 2)
    assert_array_almost_equal(oobs[2].area, 1)
    assert_array_almost_equal(oobs[3].area, 1)
    assert_array_almost_equal(oobs[4].area, 0)