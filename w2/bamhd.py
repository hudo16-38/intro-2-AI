import json
import sys
from queue import PriorityQueue
from math import radians, cos, sin, asin, sqrt

class BaMHD(object):
    def __init__(self, db_file='ba_mhd_db.json'):
        # Initialize BaMHD object, load data from json file
        self.data = json.load(open(db_file, 'r'))

    def distance(self, stop1, stop2):
        # Return distance between two stops in km.
        if isinstance(stop1, BusStop): stop1 = stop1.name
        if isinstance(stop2, BusStop): stop2 = stop2.name
        coords1 = self.data['bus_stops'][stop1]
        coords2 = self.data['bus_stops'][stop2]

        def haversine(lon1, lat1, lon2, lat2):
            # (You don`t need to understand following code - it`s just geo-stuff)
            # Calculate the great circle distance between two points on the earth (specified in
            # decimal degrees)
            # Courtesy of http://stackoverflow.com/a/15737218

            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            km = 6367 * c
            return km

        return haversine(coords1[0], coords1[1], coords2[0], coords2[1])

    def neighbors(self, stop):
        # Return neighbors for a given stop
        return self.data['neighbors'][stop.name if isinstance(stop, BusStop) else stop]

    def stops(self):
        # Return list of all stops (names only)
        return self.data['neighbors'].keys()


class BusStop(object):
    # Object representing node in graph traversal. Includes name, parent node, and total cost of
    # path from root to this node (i.e. distance from start).
    def __init__(self, name, parent = None, pathLength = 0):
        self.name = name
        self.parent = parent
        self.pathLength = pathLength

    def traceBackPath(self):
        # Returns path represented by this node as list of node names (bus stop names).
        if self.parent == None:
            return [self.name]
        else:
            path = self.parent.traceBackPath()
            path.append(self.name)
            return path


def findPathUniformCost(bamhd, stopA, stopB):
    start_node = BusStop(stopA)
    pq = PriorityQueue()
    pq.put((0, start_node))
    visited = set()
    counter = 1

    while not pq.empty():
        path_length, node = pq.get()

        if node.name in visited: continue

        if node.name == stopB: break

        visited.add(node.name)

        for adjacent in bamhd.neighbors(node):
            dist = node.pathLength + bamhd.distance(node, adjacent)
            pq.put((dist, BusStop(adjacent, pathLength=dist, parent=node)))
            counter += 1
    else:
        return ["Route not found"]

    ### Your code here ###
    print('\t{} bus stops in "OPEN list", length = {}km'.format(counter, round(node.pathLength, 2)))
    return node.traceBackPath()


def findPathAStar(bamhd, stopA, stopB):
    start_node = BusStop(stopA)
    pq = PriorityQueue()
    pq.put((0, start_node))
    visited = set()
    counter = 1

    while not pq.empty():
        path_length, node = pq.get()

        if node.name in visited: continue

        if node.name == stopB: break

        visited.add(node.name)

        for adjacent in bamhd.neighbors(node):
            dist1 = node.pathLength + bamhd.distance(node, adjacent)
            dist2 = bamhd.distance(adjacent, stopB)
            pq.put((dist1+dist2, BusStop(adjacent, pathLength=dist1, parent=node)))
            counter += 1
    else:
        return ["Route not found"]


    print('\t{} bus stops in "OPEN list", length = {}km'.format(counter, round(node.pathLength, 2)))
    return node.traceBackPath()
    


if __name__ == "__main__":
    # Initialization
    bamhd = BaMHD()
    #print("zastavky",bamhd.stops())
   # print([bus for bus in bamhd.stops() if bus.startswith("Cintorin")])

    # Your task: find best route between two stops with:
    # A) Uniform-cost search
    print('Uniform-cost search:')
    print('Zoo - Aupark:')
    path = findPathUniformCost(bamhd, 'Zoo', 'Aupark')
    print('\tpath: {}'.format(path))
    print()

    print('VW - Astronomicka:')
    path = findPathUniformCost(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath: {}'.format(path))
    print()

    print("Cintorin Slavicie udolie - Hlavna stanica")
    path =  findPathUniformCost(bamhd, 'Cintorin Slavicie udolie', 'Hlavna stanica')
    print('\tpath: {}'.format(path))
    print()

    # B) A* search
    print('\nA* search:')
    print('Zoo - Aupark:')
    path = findPathAStar(bamhd, 'Zoo', 'Aupark')
    print('\tpath: {}'.format(path))
    print()

    print('VW - Astronomicka:')
    path = findPathAStar(bamhd, 'Volkswagen', 'Astronomicka')
    print('\tpath: {}'.format(path))
    print()

    print("Cintorin Slavicie udolie - Hlavna stanica")
    path = findPathAStar(bamhd, 'Cintorin Slavicie udolie', 'Hlavna stanica')
    print('\tpath: {}'.format(path))
