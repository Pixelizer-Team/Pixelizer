import math


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
            counter += 1
            xs += w
        ys += yoffset
        row += 1
    return polygons


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
            counter += 1
            xs += w
        ys += yoffset
        row += 1
    return polygons
