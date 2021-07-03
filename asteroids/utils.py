import pygame

def points_to_lines(position, points):
    """
    Take a central position and a list of surrounding x,y coordinates, and
    convert them into a tuple representing lines
    """

    lines = []
    for index, point in enumerate(points):
        try:
            next_point = points[index + 1]
        except IndexError:
            next_point = points[0]

        first_point = pygame.math.Vector2(position)
        first_point.from_polar(point)
        first_point = position + first_point

        second_point = pygame.math.Vector2(position)
        second_point.from_polar(next_point)
        second_point = position + second_point

        lines.append((first_point, second_point))

    return lines

def bresenham(start, end):
    """
    Based on https://github.com/encukou/bresenham/blob/master/bresenham.py

    Given two points, this function will return a list of all points that
    exist between the two.
    """

    x1, y1 = int(start.x), int(start.y)
    x2, y2 = int(end.x), int(end.y)

    dx = x2 - x1
    dy = y2 - y1

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield x1 + x*xx + y*yx, y1 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

def lines_intersect(line1, line2):
    """
    Return True if two lines intersect, otherwise return False
    https://stackoverflow.com/a/9997374
    """
    def ccw(a, b, c):
        return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

    a, b = line1
    c, d = line2
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)
