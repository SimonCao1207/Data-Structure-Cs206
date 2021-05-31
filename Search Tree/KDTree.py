import math
import sys

def distance(point1, point2):
	x1, y1 = point1
	x2, y2 = point2

	dx = x1 - x2
	dy = y1 - y2
	return math.sqrt(dx*dx + dy*dy)

def closest_point(all_points, new_point):
    best_point = None
    best_distance = None
    for current_point in all_points:
        current_distance = distance(current_point, new_point)
        if best_distance is None or current_distance < best_distance:
            best_distance = current_distance
            best_point = current_point
    return best_point

k = 2

def build_kdtree(points, depth = 0):
    n = len(points)
    if n<=0:
        return None
    axis = depth % k
    sorted_points = sorted(points, key=lambda point: point[axis])
    return {
        'point': sorted_points[n//2],
        'left': build_kdtree(sorted_points[:n//2], depth + 1),
        'right': build_kdtree(sorted_points[n//2 + 1:], depth + 1)
    }


def closer_distance(pivot, p1, p2):
    if p1 is None:
        return p2

    if p2 is None:
        return p1

    d1 = distance(pivot, p1)
    d2 = distance(pivot, p2)

    if d1 < d2:
        return p1
    else:
        return p2


def kdtree_closest_point(root, point, depth=0):
    if root is None:
        return None

    axis = depth % k

    next_branch = None
    opposite_branch = None

    if point[axis] < root['point'][axis]:
        next_branch = root['left']
        opposite_branch = root['right']
    else:
        next_branch = root['right']
        opposite_branch = root['left']

    best = closer_distance(point,
                           kdtree_closest_point(next_branch,
                                                point,
                                                depth + 1),
                           root['point'])

    if distance(point, best) ** 2 > (point[axis] - root['point'][axis]) ** 2:
        best = closer_distance(point,
                               kdtree_closest_point(opposite_branch,
                                                    point,
                                                    depth + 1),
                               best)

    return best

def visitPlanet(all_points, visit=[], pivot=(0,0)):
    if len(all_points)==0:
        return visit
    kdtree = build_kdtree(all_points)
    found = kdtree_closest_point(kdtree, pivot)
    print(found)
    visit.append(found)
    new_lst = [x for x in all_points if x!= found]
    visitPlanet(new_lst, visit, found)


def main():    

    N = 8
    lst = [(2,1), (2,0), (2,2), (4,-1), (5,0), (3,3), (5,-2), (3,-1)]
    # kdtree = build_kdtree(lst)
    # pivot = (0,0)
    # found = kdtree_closest_point(kdtree, pivot)
    # print(found)

    visit_lst = visitPlanet(lst)
    print(visit_lst)

if __name__ =='__main__':
    main()