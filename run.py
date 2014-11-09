"""Main function. Uses the other files to simulate google tracking other
cars."""

from __future__ import division
from cars import addCar
import topology
from random import randint


def moveCars(topo, timeStep, trackingInfo):
    """Go through each node in topo. While there are still cars in a node that
    haven't yet moved, go through them and move them. If a car has arrived at
    it's destination, remove it."""
    for node in topo:
        if node._cars:
            while node._cars and node._cars[0]._timeStep == timeStep:
                car = node._cars.pop(0)  # Remove first car from list
                car._timeStep += 1  # Advance timestep
                # Look at where we are along in the car's trip.
                position = car._trip.index(node._nodeID)
                # If we are at the end of our trip..
                if position + 1 == len(car._trip):
                    trackingInfo[0].append(car)
                    if not car._goog:
                        trackingInfo[3] += len(car._trip)
                else:
                    topo[car._trip[position + 1]]._cars.append(car)


def cleanup(topo, trackingInfo):
    """Go through all the cars and add their current position on their journey
    to trackingInfo."""
    for node in topo:
        if node._cars:
            while node._cars:
                car = node._cars.pop(0)
                if not car._goog:
                    position = car._trip.index(node._nodeID)
                    trackingInfo[3] += position


def trackCars(topo, trackedInfo, timeStep):
    """Check each node for a google car. If a google car is present, then track
    the other cars."""

    for node in topo:
        for car in node._cars:
            if car._goog:
                for car in node._cars:
                    if not car._goog:
                        info = [timeStep, car._carID, node._nodeID]
                        trackedInfo.append(info)
                break


def trackCarsShort(topo, trackedInfo, trackingInfo, timeStep):
    """Check each node for a google car. If a google car is present, then track
    the other cars. If there are no google cars in a given node, then that
    means all the cars in that node are non-google cars, and thus untrackable.
    So we remove them from the pool of possible tracked cars."""

    for node in topo:
        for car in node._cars:
            if car._goog:
                for car in node._cars:
                    if not car._goog:
                        info = [timeStep, car._carID, node._nodeID]
                        trackedInfo.append(info)
                break
        else:
            while node._cars:
                car = node._cars.pop(0)
                trackingInfo[3] += len(car._trip)


def simulate(timesteps=5000, googChance=0.5, size=50):
    timeStep = 0
    trackingInfo = [[], [], 0, 0]
    trackedInfo = []
    carID = 0
    topo, paths = topology.topomake(size)

    for i in xrange(timesteps):
        for j in xrange(len(topo)):
            for k in range(randint(0, 3)):
                car = addCar(topo, paths, googChance, carID, timeStep, j)
                if car._goog:
                    trackingInfo[2] += 1
                trackingInfo[1].append(car)
                carID += 1
        trackCars(topo, trackedInfo, timeStep)
        moveCars(topo, timeStep, trackingInfo)
        timeStep += 1
    cleanup(topo, trackingInfo)
    return trackingInfo, trackedInfo

if __name__ == '__main__':
    goog = float(raw_input('GoogChance [default=50]: ') or 50)/100
    n = int(raw_input('Size [default=50]: ') or 50)
    trackingInfo, trackedInfo = simulate(googChance=goog, size=n)
    print "===================="
    print "Total cars: " + repr(len(trackingInfo[1]))
    print "Number of google cars: " + repr(trackingInfo[2])
    print "Actual number of observed car/location/time tuples: "\
          + repr(len(trackedInfo))
    print "Total number of tuples: " + repr(trackingInfo[3])
    print ""
    print "Percentage tracked: " + repr(len(trackedInfo)/trackingInfo[3])
