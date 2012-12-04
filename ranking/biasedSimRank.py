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

graph = pickle.load(open('user-file-graph'))
score = pickle.load(open('simrank.pickled'))

lDevelopers = []
for node in graph.nodes(data=True):
    if (node[1]['type']=='Developer'): lDevelopers.append(node[0])

for i in range(len(lDevelopers)):
    for j in range(i+1, len(lDevelopers)):
        print lDevelopers[i], lDevelopers[j], score[(lDevelopers[i],lDevelopers[j])] * pow(len(graph.neighbors(lDevelopers[j])), popularityBias)
        print lDevelopers[j], lDevelopers[i], score[(lDevelopers[i],lDevelopers[j])] * pow(len(graph.neighbors(lDevelopers[i])), popularityBias)
