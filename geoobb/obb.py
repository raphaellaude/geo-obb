"""
This module contains functions for calculating the oriented bounding box of width geometry.
"""

import numpy as np
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Point, Polygon, MultiPolygon, GeometryCollection


def pca_eigenvectors(pts: np.ndarray) -> np.ndarray:
    """
    Returns the principal axes of a set of points.
    Method is essentially running a PCA on the points.

    Parameters
    ----------
    pts : array_like
    """
    ca = np.cov(pts, y=None, rowvar=False, bias=True)
    val, vect = np.linalg.eig(ca)

    return np.transpose(vect)


def oriented_bounding_box(pts: np.ndarray) -> np.ndarray:
    """
    Returns the oriented bounding box width set of points.

    Based on [Create the Oriented Bounding-box (OBB) with Python and NumPy](https://stackoverflow.com/questions/32892932/create-the-oriented-bounding-box-obb-with-python-and-numpy).

    Parameters
    ----------
    pts : array_like
    """
    tvect = pca_eigenvectors(pts)
    rot_matrix = np.linalg.inv(tvect)

    rot_arr = np.dot(pts, rot_matrix)

    mina = np.min(rot_arr, axis=0)
    maxa = np.max(rot_arr, axis=0)
    diff = (maxa - mina) * 0.5

    center = mina + diff

    half_w, half_h = diff
    corners = np.array([
        center + [-half_w, -half_h],
        center + [half_w, -half_h],
        center + [half_w, half_h],
        center + [-half_w, half_h],
    ])

    return np.dot(corners, tvect)


def oriented_bounding_box_dimensions(pts: np.ndarray) -> np.ndarray:
    """
    Returns the dimensions of the oriented bounding box width set of points.

    Parameters
    ----------
    pts : array_like
    """
    tvect = pca_eigenvectors(pts)
    rot_matrix = np.linalg.inv(tvect)

    rot_arr = np.dot(pts, rot_matrix)

    mina = np.min(rot_arr, axis=0)
    maxa = np.max(rot_arr, axis=0)

    return np.abs(np.dot(maxa - mina, tvect))


## OBB Utilities


def polygon_from_obb(obb: np.ndarray) -> Polygon:
    """
    Returns the oriented bounding box width set of points.

    Parameters
    ----------
    obb : array_like
    """
    obb = np.vstack((obb, obb[0]))
    return Polygon(obb)


def obb_angle(obb: np.ndarray) -> float:
    """
    Returns the angle of the oriented bounding box width set of points.

    Parameters
    ----------
    obb : array_like
    """
    distances = [np.linalg.norm(obb[i] - obb[(i + 1) % 4]) for i in range(4)]
    long_edge_index = np.argmax(distances)
    p1, p2 = obb[long_edge_index], obb[(long_edge_index + 1) % 4]
    long_edge_vector = p2 - p1
    angle = np.arctan2(long_edge_vector[1], long_edge_vector[0])
    
    return angle


## Geometry Utilities


def geom_to_array(geom: BaseGeometry, omit_last=True) -> np.ndarray:
    """
    Prepares the geometry as an array.

    Parameters
    ----------
    geom : shapely geometry
    """
    n = -1 if omit_last else None
    if isinstance(geom, Polygon):
        return np.array(geom.exterior.coords[:n])
    elif isinstance(geom, MultiPolygon):
        return np.vstack([np.array(p.exterior.coords[:n]) for p in geom.geoms])
    return np.array(geom.coords[:n])


def geom_to_unique_array(geom: BaseGeometry) -> np.ndarray:
    """
    Prepares the geometry for the oriented bounding box calculation.

    Parameters
    ----------
    geom : shapely geometry
    """
    arr = geom_to_array(geom)
    return np.unique(arr, axis=0)
