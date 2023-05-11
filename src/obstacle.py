def is_passing_through_obstaicle(p1, p2, r1, r2):
    x1, y1 = p1
    x2, y2 = p2
    x_min, y_min = r1
    x_max, y_max = r2
    
    # Trouver les coordonnées des points d'intersection entre le segment et les côtés du rectangle
    intersections = []
    if x_min <= x1 <= x_max and y_min <= y1 <= y_max:
        intersections.append((x1, y1))
    if x_min <= x2 <= x_max and y_min <= y2 <= y_max:
        intersections.append((x2, y2))
    if y_min <= y1 <= y_max:
        x = x_min if x1 < x_min else x_max if x1 > x_max else x1
        intersections.append((x, y1))
    if y_min <= y2 <= y_max:
        x = x_min if x2 < x_min else x_max if x2 > x_max else x2
        intersections.append((x, y2))
    
    # Vérifier si l'un des points d'intersection est à la fois à l'intérieur du rectangle et sur le segment
    for x, y in intersections:
        if x_min < x < x_max and y_min < y < y_max:
            if (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1) == 0:
                return True
    
    return False