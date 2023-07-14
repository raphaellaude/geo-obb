"""
This module contains functions for calculating the oriented bounding box of a geometry.
"""

import numpy as np
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, Point, MultiPoint


def geom_to_array(geom: Polygon or MultiPolygon or LineString or MultiLineString or Point or MultiPoint) -> np.ndarray:
    """
    Prepares the geometry for the oriented bounding box calculation.

    Parameters
    ----------
    geom : any shapely geometry type
    """
    if isinstance(geom, Polygon) or isinstance(geom, MultiPolygon):
        x = np.array(geom.exterior.coords)
    else:
        x = np.array(geom.coords)
    return np.unique(x, axis=0)


def oriented_bounding_box(pts: np.ndarray) -> np.ndarray:
    """
    Returns the oriented bounding box a set of points.

    Based on [Create the Oriented Bounding-box (OBB) with Python and NumPy](https://stackoverflow.com/questions/32892932/create-the-oriented-bounding-box-obb-with-python-and-numpy).

    Parameters
    ----------
    pts : array_like
    """
    ca = np.cov(pts, y=None, rowvar=False, bias=True)

    val, vect = np.linalg.eig(ca)
    tvect = np.transpose(vect)

    #use the inverse of the eigenvectors as a rotation matrix and
    #rotate the points so they align with the x and y axes
    arr = np.dot(pts, np.linalg.inv(tvect))

    # get the minimum and maximum x and y
    mina = np.min(arr, axis=0)
    maxa = np.max(arr, axis=0)
    diff = (maxa - mina) * 0.5

    # the center is just half way between the min and max xy
    center = mina + diff

    #get the 4 corners by subtracting and adding half the bounding boxes height and width to the center
    a, b = diff
    corners = np.array([
        center + [-a, -b], center + [a, -b], center + [a, b], center + [-a, b],
        center + [-a, -b]
    ])

    #use the the eigenvectors as a rotation matrix and
    #rotate the corners and the centerback
    corners = np.dot(corners, tvect)
    center = np.dot(center, tvect)

    return corners


def oriented_bb_center_diff(pts: np.ndarray):
    """
    """
    val, vect = np.linalg.eig(np.cov(pts, y=None, rowvar=False, bias=True))
    tvect = np.transpose(vect)

    #use the inverse of the eigenvectors as a rotation matrix and
    #rotate the points so they align with the x and y axes
    arr = np.dot(pts, np.linalg.inv(tvect))

    # get the minimum and maximum x and y
    mina = np.min(arr, axis=0)
    maxa = np.max(arr, axis=0)
    diff = (maxa - mina) * 0.5

    # the center is just half way between the min and max xy
    center = mina + diff

    return center, diff
