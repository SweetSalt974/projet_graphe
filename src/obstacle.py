def get_rectangle_edges(rectangle):
    a = (rectangle[0][0], rectangle[0][1])
    b = (rectangle[1][0], rectangle[0][1])
    c = (rectangle[0][0], rectangle[1][1])
    d = (rectangle[1][0], rectangle[1][1])
    return [(a, b), (a, c), (b, d), (c, d)]

def intersection(segment1, segment2):
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]
    
    if (x1, y1) == (x3, y3) and (x2, y2) == (x4, y4):
        return False

    a1, b1, c1 = y2 - y1, x1 - x2, x2*y1 - x1*y2
    a2, b2, c2 = y4 - y3, x3 - x4, x4*y3 - x3*y4
    
    det = a1*b2 - a2*b1
    if det == 0:
        # les droites sont parallèles
        return False
    x = (b2*c1 - b1*c2) / det
    y = (a1*c2 - a2*c1) / det

    x = abs(x)
    y = abs(y)
    
    if (min(x1, x2) <= x <= max(x1, x2) and
        min(y1, y2) <= y <= max(y1, y2) and
        min(x3, x4) <= x <= max(x3, x4) and
        min(y3, y4) <= y <= max(y3, y4)):
        # le point d'intersection est à l'intérieur des deux segments
        if ((x, y) != (x1, y1) and (x, y) != (x2, y2) and
            (x, y) != (x3, y3) and (x, y) != (x4, y4)):
            return True
    return False

def is_passing_through_obstacle(p1, p2, rectangle):
    rectangle_sides = get_rectangle_edges(rectangle)
    if (p1 == rectangle_sides[0][0] and p2 == rectangle_sides[3][1]) or (p1 == rectangle_sides[0][1] and p2 == rectangle_sides[1][1]):
        return True
    for side in get_rectangle_edges(rectangle):
        if (intersection((p1,p2), side)):
            return True
    return False

def is_passing_through_any_obstacle(p1, p2, rectangles):
    for rectangle in rectangles:
        if is_passing_through_obstacle(p1, p2, rectangle):
            return rectangle
    return None