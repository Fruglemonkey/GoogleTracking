"""Main function. Uses the other files to simulate google tracking other cars."""
from __future__ import division
from cars import Car, addCar
import topology
from random import randint

def moveCars(topo, timeStep, trackingInfo):
    for node in topo:
        if node._cars:
            while node._cars and node._cars[0]._timeStep == timeStep:
                car = node._cars.pop(0)  # Remove first car from list
                car._timeStep += 1  # Advance timestep
                # Look at where we are along in the car's trip.
                position = car._trip.index(node._nodeID)
                if position + 1 == len(car._trip):  # If we are at the end of our trip..
                    # print "Car " + repr(car._carID) + " Leaving!"
                    trackingInfo[0].append(car)
                else:
                    topo[car._trip[position + 1]]._cars.append(car)


def trackCars(topo, trackedInfo, timeStep):
    for node in topo:
        for car in node._cars:
            if car._goog:
                for car in node._cars:
                    if not car._goog:
                        info = [timeStep, car._carID, node._nodeID]
                        trackedInfo.append(info)
                break

googChance = float(raw_input('GoogChance [default=50]: ') or 50)/100
timeStep = 0
trackingInfo = [[], [], 0]  # [0] is cars that left, [1] is all cars, [2] is number of goog cars
trackedInfo = []
carID = 0
n = int(raw_input('Size [default=50]: ') or 50) 
topo, paths = topology.topomake(n)
# print " " + repr(range(n))
# for x, y in enumerate(topo):
#     print repr(x) + repr(y._nextHops)

for i in xrange(500):
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

# for bit in trackedInfo:




#for node in topo:
#    print "There are " + repr(len(node._cars)) + " cars at this node"
#    for car in node._cars:
#        print "Start: " + repr(node._nodeID)
#        car.printInfo()
summingtotal = 0
for node in paths:
    for path in node:
        summingtotal += len(path)
average = summingtotal/n**2
print "Average path length: " + repr(average)
print "Total cars: " + repr(carID)
print "Number of google cars: " + repr(trackingInfo[2])
print "Actual number of observed car/location/time tuples: " + repr(len(trackedInfo))
print "Expected number: " + repr(average * (carID - trackingInfo[2]))
print "\nNote: This number should be higher than the number observed, because \n" \
      "There are still cars in system when simulation ends."
print "\nPercentage of tracked datapoints: " + repr(len(trackedInfo)/(average * (carID - trackingInfo[2])))
print ""
print "Longest path: " + repr(topology.findLongestPath(paths))
