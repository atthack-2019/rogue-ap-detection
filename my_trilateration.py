import numpy as np
import itertools


GOOD_DIST = 200

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


c1 = Circle(407,222,152.0182738030424)
c2 = Circle(546,395,78.7322553235653)
c3 = Circle(83,110,259.53757108554686)
c4 = Circle(631,312,10.253201506510855)
c6 = Circle(206,877,756.4734324616041)
#circle_ls = [c1, c2, c3, c4, c6]
circle_ls = [Circle(224, 288, 155.80939351149925), Circle(394, 162, 113.9857424979084), Circle(778, 65, 1405.852596769204), Circle(111, 614, 237.08172378776163), Circle(313, 65, 16.655486892608547), Circle(394, 162, 99.73903144672268), Circle(877, 490, 691.0214371565008), Circle(224, 288, 112.81641809805299), Circle(778, 65, 940.209191153721), Circle(877, 490, 1593.574262133578)]

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

print("INTERSECTION POINTS")
print(calculate_intersection_points(circle_ls))
p_list = calculate_intersection_points(circle_ls)

def find_smallest_circle(circle_list):
    min_circle = circle_list[0]
    for circle in circle_list:
        if circle.radius <= min_circle.radius:
            min_circle = circle
    return min_circle

smallest_circle = find_smallest_circle(circle_ls)

def remove_invalid_intersections(point_list, smallest_circle):
    result = []
    for point in point_list:
        dist_x, dist_y = smallest_circle.x - point[0], smallest_circle.y - point[1]
        dist = np.sqrt(dist_x**2 + dist_y ** 2)
        if dist < GOOD_DIST:
            result.append(point)
    return result
res = remove_invalid_intersections(p_list,smallest_circle)

def get_mean_location(point_list):
    x_loc = .0
    y_loc = .0
    for x, y in point_list:
        x_loc += x
        y_loc += y
    x_loc /= float(len(point_list))
    y_loc /= float(len(point_list))
    return (x_loc, y_loc)

print("MEAN LOCATION: \n")
print(get_mean_location(res))
