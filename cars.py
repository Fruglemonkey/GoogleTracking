"""Car functions + object."""
from random import randint, random
import topology


class Car(object):

    """A car in my network."""

    def __init__(self, carID, destination, trip, timeStep, goog):
        """Initialises a car.

        :carID: The identifier for the car
        :destination: The destination node for the car
        :trip: The trip length of the car's journey. Used to
        calculate if a car has been tracked for the full length of it's
        journey.
        :timeStep: The current timestep that the car is in. Used to help
        iterate over the timesteps.

        """
        self._carID = carID
        self._destination = destination
        self._trip = trip
        self._timeStep = timeStep
        self._goog = goog
    
    def printInfo(self):
        print "carID: " + repr(self._carID)
        print "Destination: " + repr(self._destination)
        print "Trip: " + repr(self._trip)
        print "timeStep: " + repr(self._timeStep)
        print ""

def addCar(topo, paths, googChance, ID, timestep, start=-1):
    """Add a car to a node in the topology. If no node is specified, add the
    car to a random node instead."""
    dest = randint(0, len(topo) - 1)
    if random() < googChance:
        goog = 1
    else:
        goog = 0
    if start != -1:
        car = Car(ID, dest, paths[start][dest], timestep, goog)
        topo[start]._cars.append(car)
        return car
    else:
        start = randint(0, len(topo) - 1)
        car = Car(ID, dest, paths[start][dest], timestep, goog)
        topo[start]._cars.append(car)
        return car

if __name__ == '__main__':
    """Demonstrates that adding a car to the topology works. Adds a car randomly
    as well as adding one to node 0."""
    n = int(input('size? '))
    topo, paths = topology.topomake(n)
    print " " + repr(range(n))
    for x, y in enumerate(topo):
        print repr(x) + repr(y._nextHops)
    addCar(topo, paths, .5, 1, 1)
    addCar(topo, paths, .5, 1, 1, 0)
    for node in topo:
        for car in node._cars:
            print "Start: " + repr(node._nodeID)
            print "Destination: " + repr(car._destination)
            print "Trip: " + repr(car._trip)
