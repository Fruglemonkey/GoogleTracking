"""Takes the graph generated by graphmake and turns it into a custom topology.
"""

import graphmake


class Node(object):

    """A node for my custom topology"""

    def __init__(self, nodeID, size):
        """Each node has a list of next-hops.

        :nodeID: Node ID.
        :size: Size of the graph. Used to create nextHops
        """
        self._nodeID = nodeID
        self._nextHops = [None] * size
        self._cars = []

    def addNextHop(self, path, dest):
        """Given a path to dest, add the next hop to that path"""
        if len(path) == 1:
            # If the length of your path is one, your next hop is to stay here!
            self._nextHops[self._nodeID] = self._nodeID
        else:
            self._nextHops[dest] = path[1]


def topomake(nodes):
    """There are :nodes: number of nodes.
    nodes = [[] for x in range(nodes)]"""
    topo = [None] * nodes
    graph = graphmake.graphgen(nodes)
    paths = graphmake.pathgen(graph)
    for i in range(nodes):
        topo[i] = Node(i, nodes)
    # For each node, add the next hop to each other node.
    for i in range(nodes):
        for j in range(nodes):
            topo[i].addNextHop(paths[i][j], j)
    return topo, paths


if __name__ == '__main__':
    n = int(input('size? '))
    topo = topomake(n)
    print " " + repr(range(n))
    for x, y in enumerate(topo):
        print repr(x) + repr(y._nextHops)
