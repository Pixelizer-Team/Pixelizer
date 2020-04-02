import math
import numpy as np


def hexagon_tile(xs, ys, xe, ye, radius):
    """
    Calculate a grid of hexagon coordinates of the given radius
    given lower-left and upper-right coordinates
    Returns a list of lists containing 6 tuples of x, y point coordinates
    These can be used to construct valid regular hexagonal polygons

    You will probably want to use projected coordinates for this
    """
    # calculate side length given radius
    sl = (2 * radius) * math.tan(math.pi / 6)
    # calculate radius for a given side-length
    # (a * (math.cos(math.pi / 6) / math.sin(math.pi / 6)) / 2)
    # see http://www.calculatorsoup.com/calculators/geometry-plane/polygon.php

    # calculate coordinates of the hexagon points
    # sin(30)
    p = sl * 0.5
    b = sl * math.cos(math.radians(30))
    w = b * 2
    h = 2 * sl

    # offset start and end coordinates by hex widths and heights to guarantee coverage
    xs = xs - w
    ys = ys - h
    xe = xe + w
    ye = ye + h

    origx = xs
    origy = ys

    # offsets for moving along and up rows
    xoffset = b
    yoffset = 3 * p

    polygons = []
    weights = []

    row = 1
    counter = 0

    while ys < ye:
        if row % 2 == 0:
            xs = origx + xoffset
        else:
            xs = origx
        while xs < xe:
            p1x = xs
            p1y = ys + p
            p2x = xs
            p2y = ys + (3 * p)
            p3x = xs + b
            p3y = ys + h
            p4x = xs + w
            p4y = ys + (3 * p)
            p5x = xs + w
            p5y = ys + p
            p6x = xs + b
            p6y = ys
            poly = [
                (p1x, p1y),
                (p2x, p2y),
                (p3x, p3y),
                (p4x, p4y),
                (p5x, p5y),
                (p6x, p6y),
                (p1x, p1y)]
            polygons.append(poly)
            weights.append(1)
            counter += 1
            xs += w
        ys += yoffset
        row += 1
    return polygons, weights


def cubic_tile(xs, ys, xe, ye, radius):
    """
    Calculate a grid of cubic coordinates of the given radius
    given lower-left and upper-right coordinates
    Returns a list of lists containing 4 tuples of x, y point coordinates
    These can be used to construct valid regular cubic polygons

    You will probably want to use projected coordinates for this
    """
    # calculate side length given radius
    sl = (2 * radius) * math.tan(math.pi / 6)
    # calculate radius for a given side-length
    # (a * (math.cos(math.pi / 6) / math.sin(math.pi / 6)) / 2)
    # see http://www.calculatorsoup.com/calculators/geometry-plane/polygon.php

    # calculate coordinates of the hexagon points
    # sin(30)
    p = sl * 0.5
    b = sl * math.cos(math.radians(30))
    w = b * 2
    h = 2 * sl

    # offset start and end coordinates by hex widths and heights to guarantee coverage
    xs = xs - w
    ys = ys - h
    xe = xe + w
    ye = ye + h

    origx = xs
    origy = ys

    # offsets for moving along and up rows
    xoffset = b
    yoffset = 3 * p

    polygons = []
    weights = []

    row = 1
    counter = 0

    while ys < ye:
        if row % 2 == 0:
            xs = origx + xoffset
        else:
            xs = origx
        while xs < xe:
            p1x = xs
            p1y = ys + p
            p2x = xs
            p2y = ys + (3 * p)
            p3x = xs + b
            p3y = ys + h
            p4x = xs + w
            p4y = ys + (3 * p)
            p5x = xs + w
            p5y = ys + p
            p6x = xs + b
            p6y = ys
            cx = (p1x + p3x + p5x) / 3
            cy = (p1y + p3y + p5y) / 3
            poly1 = [
                (p1x, p1y),
                (p2x, p2y),
                (cx, cy),
                (p6x, p6y),
            ]
            poly2 = [
                (p2x, p2y),
                (p3x, p3y),
                (p4x, p4y),
                (cx, cy),
            ]
            poly3 = [
                (p4x, p4y),
                (p5x, p5y),
                (p6x, p6y),
                (cx, cy),
            ]
            polygons.append(poly1)
            polygons.append(poly2)
            polygons.append(poly3)
            weights.append(1.0)
            weights.append(0.8)
            weights.append(0.6)
            counter += 1
            xs += w
        ys += yoffset
        row += 1
    return polygons, weights


def double_cubic_tile(xs, ys, xe, ye, radius):
    """
    Calculate a grid of cubic coordinates of the given radius
    given lower-left and upper-right coordinates
    Returns a list of lists containing 4 tuples of x, y point coordinates
    These can be used to construct valid regular cubic polygons

    You will probably want to use projected coordinates for this
    """
    # calculate side length given radius
    sl = (2 * radius) * math.tan(math.pi / 6)
    # calculate radius for a given side-length
    # (a * (math.cos(math.pi / 6) / math.sin(math.pi / 6)) / 2)
    # see http://www.calculatorsoup.com/calculators/geometry-plane/polygon.php

    # calculate coordinates of the hexagon points
    # sin(30)
    p = sl * 0.5
    b = sl * math.cos(math.radians(30))
    w = b * 2
    h = 2 * sl

    # offset start and end coordinates by hex widths and heights to guarantee coverage
    xs = xs - w
    ys = ys - h
    xe = xe + w
    ye = ye + h

    origx = xs
    origy = ys

    # offsets for moving along and up rows
    xoffset = b
    yoffset = 3 * p

    polygons = []
    weights = []

    row = 1
    counter = 0

    while ys < ye:
        if row % 2 == 0:
            xs = origx + xoffset
        else:
            xs = origx
        while xs < xe:
            p1x = xs
            p1y = ys + p
            p2x = xs
            p2y = ys + (3 * p)
            p3x = xs + b
            p3y = ys + h
            p4x = xs + w
            p4y = ys + (3 * p)
            p5x = xs + w
            p5y = ys + p
            p6x = xs + b
            p6y = ys
            cx = (p1x + p3x + p5x) / 3
            cy = (p1y + p3y + p5y) / 3

            p1x_i = 0.5 * (p1x + cx)
            p2x_i = 0.5 * (p2x + cx)
            p3x_i = 0.5 * (p3x + cx)
            p4x_i = 0.5 * (p4x + cx)
            p5x_i = 0.5 * (p5x + cx)
            p6x_i = 0.5 * (p6x + cx)
            p1y_i = 0.5 * (p1y + cy)
            p2y_i = 0.5 * (p2y + cy)
            p3y_i = 0.5 * (p3y + cy)
            p4y_i = 0.5 * (p4y + cy)
            p5y_i = 0.5 * (p5y + cy)
            p6y_i = 0.5 * (p6y + cy)

            poly1 = [
                (p1x_i, p1y_i),
                (p2x_i, p2y_i),
                (cx, cy),
                (p6x_i, p6y_i),
            ]
            weights.append(1.0)
            poly2 = [
                (p2x_i, p2y_i),
                (p3x_i, p3y_i),
                (p4x_i, p4y_i),
                (cx, cy),
            ]
            weights.append(0.8)
            poly3 = [
                (p4x_i, p4y_i),
                (p5x_i, p5y_i),
                (p6x_i, p6y_i),
                (cx, cy),
            ]
            weights.append(0.6)
            polygons.append(poly1)
            polygons.append(poly2)
            polygons.append(poly3)

            poly4 = [
                (p1x, p1y),
                (p2x, p2y),
                (p3x, p3y),
                (p3x_i, p3y_i),
                (p2x_i, p2y_i),
                (p1x_i, p1y_i),
            ]
            poly5 = [
                (p3x, p3y),
                (p4x, p4y),
                (p5x, p5y),
                (p5x_i, p5y_i),
                (p4x_i, p4y_i),
                (p3x_i, p3y_i),
            ]
            poly6 = [
                (p5x, p5y),
                (p6x, p6y),
                (p1x, p1y),
                (p1x_i, p1y_i),
                (p6x_i, p6y_i),
                (p5x_i, p5y_i),
            ]
            polygons.append(poly4)
            weights.append(0.6)
            polygons.append(poly5)
            weights.append(1.0)
            polygons.append(poly6)
            weights.append(0.8)

            counter += 1
            xs += w
        ys += yoffset
        row += 1
    return polygons, weights


def the_wall_tile(xs, ys, xe, ye, radius):
    polygons = []
    weights = []
    x = xs
    counter = 0
    while x < xe:
        y_start = ys if counter % 2 == 0 else ys - radius
        counter += 1
        y = y_start
        while y < ye:
            p1x = x
            p1y = y
            p2x = x
            p2y = y + 2 * radius
            p3x = x + radius
            p3y = p2y
            p4x = p3x
            p4y = y
            poly = [
                (p1x, p1y),
                (p2x, p2y),
                (p3x, p3y),
                (p4x, p4y),
            ]
            polygons.append(poly)
            weights.append(1.0)
            y += radius * 2
        x += radius

    return polygons, weights


def pyramid_tile(xs, ys, xe, ye, radius):
    polygons = []
    weights = []
    x = xs
    margin = max(2, radius / 5) / radius
    shining = 3
    c = 0.3
    while x < xe:
        y_start = ys
        y = y_start
        while y < ye:
            p1x = x
            p1y = y
            p2x = x
            p2y = y + radius
            p3x = x + radius
            p3y = p2y
            p4x = p3x
            p4y = y
            if 2 * margin >= radius:
                alpha = 0.5
                beta = 0.5
            else:
                alpha = np.random.uniform(margin, 1 - margin)
                beta = np.random.uniform(margin, 1 - margin)
            cx = alpha * p1x + (1 - alpha) * p4x
            cy = beta * p1y + (1 - beta) * p2y

            poly1 = [
                (p1x, p1y),
                (p2x, p2y),
                (cx, cy),
            ]
            poly2 = [
                (p2x, p2y),
                (p3x, p3y),
                (cx, cy),
            ]
            poly3 = [
                (p3x, p3y),
                (p4x, p4y),
                (cx, cy),
            ]
            poly4 = [
                (p4x, p4y),
                (p1x, p1y),
                (cx, cy),
            ]
            polygons.append(poly1)
            polygons.append(poly2)
            polygons.append(poly3)
            polygons.append(poly4)
            weights.append(0.8 + c * alpha ** shining)
            weights.append(0.6 + c * beta ** shining)
            weights.append(0.4 + c * (1 - alpha) ** shining)
            weights.append(0.7 + c * (1 - beta) ** shining)
            y += radius
        x += radius

    return polygons, weights


if __name__ == '__main__':
    # a = the_wall_tile(0, 0, 100, 100, 10)
    a = double_cubic_tile(0, 0, 100, 100, 30)
    print(a)
