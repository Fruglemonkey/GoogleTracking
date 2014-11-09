from __future__ import division
import run
import numpy as np
import sys

if __name__ == '__main__':
    size = int(raw_input('size?'))
    results = [[] for x in xrange(100)]
    f = open('stats.csv', 'a')
    runs = int(raw_input('how many runs?'))
    for i in xrange(runs):
        sys.stdout.write("\r%f%%" % (i/runs))
        sys.stdout.flush()
        for j in xrange(1, 100):
            goog = j/100
            trackingInfo, trackedInfo = run.simulate(size, goog)
            recorded = len(trackedInfo)
            total = trackingInfo[3]
            percentage = recorded/total
            results[j].append(percentage)

    for chance in results[1:]:
        outstring = ",".join([repr(size), repr(results.index(chance)),
                             repr(np.mean(chance)), repr(np.std(chance))])
        outstring += '\n'
        f.write(outstring)
    f.close
