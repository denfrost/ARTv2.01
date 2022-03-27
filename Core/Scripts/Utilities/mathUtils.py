"""
Math utilities
2015, Epic Games
"""

import math

import maya.api.OpenMaya as om
import maya.cmds as cmds


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CLASSES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class KDTreeNode():
    def __init__(self, point, left, right):
        self.point = point
        self.left = left
        self.right = right

    def is_leaf(self):
        return (self.left is None and self.right is None)


class KDTreeNeighbours():
    """ Internal structure used in nearest-neighbours search.
    """

    def __init__(self, query_point, t):
        self.query_point = query_point
        self.t = t  # neighbours wanted
        self.largest_distance = 0  # squared
        self.current_best = []

    def calculate_largest(self):
        if self.t >= len(self.current_best):
            self.largest_distance = self.current_best[-1][1]
        else:
            self.largest_distance = self.current_best[self.t - 1][1]

    def add(self, point):
        sd = square_distance(point, self.query_point)
        # run through current_best, try to find appropriate place
        for i, e in enumerate(self.current_best):
            if i == self.t:
                return  # enough neighbours, this one is farther, let's forget it
            if e[1] > sd:
                self.current_best.insert(i, [point, sd])
                self.calculate_largest()
                return
        # append it to the end otherwise
        self.current_best.append([point, sd])
        self.calculate_largest()

    def get_best(self):
        return [element[0] for element in self.current_best[:self.t]]


class KDTree():
    """ KDTree implementation built from http://en.wikipedia.org/wiki/K-d_tree as a starting point

        Example usage:
            from kdtree import KDTree

            tree = KDTree.construct_from_data(data)
            nearest = tree.query(point, t=4) # find nearest 4 points
    """

    def __init__(self, data):
        def build_kdtree(point_list, depth):
            if not point_list:
                return None

            # check that all points share the same dimensions
            dim = len(point_list[0])
            for point in point_list:
                if len(point) != dim:
                    print 'KDTREE: point', point, 'does not have', dim, 'dimensions.'

            # select axis based on depth modulo tested dimension
            axis = depth % dim

            # sort point list
            point_list.sort(key=lambda point: point[axis])
            # choose the median
            median = len(point_list) / 2

            # create node and recursively construct subtrees
            node = KDTreeNode(point=point_list[median],
                              left=build_kdtree(point_list[0:median], depth + 1),
                              right=build_kdtree(point_list[median + 1:], depth + 1))
            return node

        self.root_node = build_kdtree(data, depth=0)

    @staticmethod
    def construct_from_data(data):
        tree = KDTree(data)
        return tree

    def query(self, query_point, t=1, debug=1):
        stats = {'nodes_visited': 0, 'far_search': 0, 'leafs_reached': 0}

        def nn_search(node, query_point, t, depth, best_neighbours):
            if node is None:
                return

            stats['nodes_visited'] += 1

            # if we have reached a leaf, let's add to current best neighbours,
            # (if it's better than the worst one or if there is not enough neighbours)
            if node.is_leaf():
                # statistics['leafs_reached'] += 1
                best_neighbours.add(node.point)
                return

            # this node is no leaf

            # select dimension for comparison (based on current depth)
            axis = depth % len(query_point)

            # figure out which subtree to search
            near_subtree = None  # near subtree
            far_subtree = None  # far subtree (perhaps we'll have to traverse it as well)

            # compare query_point and point of current node in selected dimension
            # and figure out which subtree is farther than the other
            if query_point[axis] < node.point[axis]:
                near_subtree = node.left
                far_subtree = node.right
            else:
                near_subtree = node.right
                far_subtree = node.left

            # recursively search through the tree until a leaf is found
            nn_search(near_subtree, query_point, t, depth + 1, best_neighbours)

            # while unwinding the recursion, check if the current node
            # is closer to query point than the current best,
            # also, until t points have been found, search radius is infinity
            best_neighbours.add(node.point)

            # check whether there could be any points on the other side of the
            # splitting plane that are closer to the query point than the current best
            if (node.point[axis] - query_point[axis]) ** 2 < best_neighbours.largest_distance:
                # statistics['far_search'] += 1
                nn_search(far_subtree, query_point, t, depth + 1, best_neighbours)

            return

        # if there's no tree, there's no neighbors
        if self.root_node is not None:
            neighbours = KDTreeNeighbours(query_point, t)
            nn_search(self.root_node, query_point, t, depth=0, best_neighbours=neighbours)
            result = neighbours.get_best()
        else:
            result = []

        # print statistics
        return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# METHODS
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def square_distance(self, pointA, pointB):
    # squared euclidean distance
    distance = 0
    dimensions = len(pointA)  # assumes both points have the same dimensions
    for dimension in range(dimensions):
        distance += (pointA[dimension] - pointB[dimension]) ** 2
    return distance


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getAngleBetween(object1, object2):

    point1 = cmds.xform(object1, t=True, q=True, ws=True)
    vector1 = om.MVector(point1)

    point2 = cmds.xform(object2, t=True, q=True, ws=True)
    vector2 = om.MVector(point2)

    dotProduct = vector1.normal() * vector2.normal()

    acos = math.acos(dotProduct)
    acos = float("{0:.6f}".format(acos))
    angle = acos * 180 / math.pi

    return angle


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getDistanceBetween(object1, object2):

    point1 = cmds.xform(object1, rp=True, q=True, ws=True)
    vector1 = om.MVector(point1)

    point2 = cmds.xform(object2, rp=True, q=True, ws=True)
    vector2 = om.MVector(point2)

    distance = om.MVector(vector1 - vector2).length()
    return distance


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def returnPercentile(incomingRange, percent, key=lambda x: x):
    floor = math.floor(percent)
    ceil = math.ceil(percent)

    if percent == 1:
        return incomingRange[1]

    if percent == 0:
        return incomingRange[0]

    d0 = key(incomingRange[int(floor)] * (ceil - percent))
    d1 = key(incomingRange[int(ceil)] * (percent - floor))

    return d0 + d1
