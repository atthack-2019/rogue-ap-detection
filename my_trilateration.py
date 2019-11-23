import numpy as np
import itertools
GOOD_DIST = 150

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def two_circles_intersection(circle1, circle2):
    dist_x, dist_y = circle2.x - circle1.x, circle2.y - circle1.y
    dist = np.sqrt(dist_x**2 + dist_y ** 2)

    if dist > circle1.radius + circle2.radius:
        #print("no I")
        return None  # no intersection
    elif dist < abs(circle1.radius - circle2.radius):
        #print("one in other")
        return None  # one in other
    elif dist == 0 and circle1.radius == circle2.radius:
        # print("identical")
        return None  # identical circles

    a = (circle1.radius**2 - circle2.radius**2 + dist**2) / (2*dist)
    h = np.sqrt(circle1.radius**2 - a**2)
    x = circle1.x + a * dist_x/dist
    y = circle1.y + a * dist_y/dist
    x3 = x + h * dist_y/dist
    y3 = y - h * dist_x/dist
    x4 = x - h * dist_y/dist
    y4 = y + h * dist_x/dist
    return (x3, y3), (x4, y4)


def calculate_intersection_points(circle_list):
    results = []
    for c1, c2 in itertools.combinations(circle_list, 2):
        points = two_circles_intersection(c1, c2)
        if points == None:
            continue
        results.append(points[0])
        results.append(points[1])
    return results


def find_smallest_circle(circle_list):
    min_circle = circle_list[0]
    for circle in circle_list:
        if circle.radius <= min_circle.radius:
            min_circle = circle
    return min_circle


def remove_invalid_intersections(point_list, smallest_circle):
    result = []
    for point in point_list:
        dist_x, dist_y = smallest_circle.x - point[0], smallest_circle.y - point[1]
        dist = np.sqrt(dist_x**2 + dist_y ** 2)
        if dist < GOOD_DIST:
            result.append(point)
    return result

def get_mean_location(point_list):
    if(len(point_list) == 0):
        return None
    x_loc = .0
    y_loc = .0
    for x, y in point_list:
        x_loc += x
        y_loc += y
    x_loc /= float(len(point_list))
    y_loc /= float(len(point_list))
    return (x_loc, y_loc)

def get_trilateration_point(circles):
    p_list = calculate_intersection_points(circles)
    smallest_circle = find_smallest_circle(circles)
    res = remove_invalid_intersections(p_list,smallest_circle)
    return get_mean_location(res)

