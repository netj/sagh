#!/usr/bin/env python
'''
Input: user-file-graph, simrank.pickled
Output: simrank-biased.txt
'''
import pickle
import sys
import math

DEFAULT_POPULARITY_BIAS = 0.5

popularityBias = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_POPULARITY_BIAS

print >>sys.stderr, "loading user-file-graph"
graph = pickle.load(open('user-file-graph'))
print >>sys.stderr, "loading simrank.pickled"
score = pickle.load(open('simrank.pickled'))

lDevelopers = []
for node in graph.nodes(data=True):
    if (node[1]['type']=='Developer'): lDevelopers.append(node[0])
numDevs = len(lDevelopers)

for i in range(numDevs):
    if i % (numDevs / 10) == 0:
        print >>sys.stderr, "%d developers done so far" % i
    # to normalize, we need 2-passes
    scores_i_upper = [None] * (numDevs - i)
    scores_i_lower = [None] * (numDevs - i)
    # first, collect the values and compute max
    for j in range(i+1, numDevs):
        scores_i_upper[j-(i+1)] = score[(lDevelopers[i],lDevelopers[j])] * pow(len(graph.neighbors(lDevelopers[j])), popularityBias)
        scores_i_lower[j-(i+1)] = score[(lDevelopers[i],lDevelopers[j])] * pow(len(graph.neighbors(lDevelopers[i])), popularityBias)
    max_upper = max(scores_i_upper)
    max_lower = max(scores_i_lower)
    # and then output normalized values
    if max_upper > 0:
        for j in range(i+1, numDevs):
            s = scores_i_upper[j-(i+1)]
            if s > 0:
                print lDevelopers[i], lDevelopers[j], scores_i_upper[j-(i+1)] / max_upper
    if max_lower > 0:
        for j in range(i+1, numDevs):
            s = scores_i_lower[j-(i+1)]
            if s > 0:
                print lDevelopers[j], lDevelopers[i], scores_i_lower[j-(i+1)] / max_lower
