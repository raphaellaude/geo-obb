"""

"""

import numpy as np
from shapely.geometry import Polygon, MultiPolygon


def oriented_bounding_box(pts):
    '''
    Returns the oriented bounding box of a polygon
    Based on https://stackoverflow.com/questions/32892932/create-the-oriented-bounding-box-obb-with-python-and-numpy

    Parameters
    ----------
    pts : array_like
    '''
    ca = np.cov(pts, y=None, rowvar=False, bias=True)

    v, vect = np.linalg.eig(ca)
    tvect = np.transpose(vect)

    #use the inverse of the eigenvectors as a rotation matrix and
    #rotate the points so they align with the x and y axes
    ar = np.dot(pts, np.linalg.inv(tvect))

    # get the minimum and maximum x and y
    mina = np.min(ar, axis=0)
    maxa = np.max(ar, axis=0)
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
