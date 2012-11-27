#!/usr/bin/env python
'''
Input: Path to pickled DF-bipartite graph
Output: Pickled Dictionary containing weighted similarity between P-P and D-D
'''
from collections import defaultdict
import pickle
import sys

#if len(sys.argv) != 2:
#    print 'usage : DF-graphCreate.py <path_to_DFgraph> \n'
#    sys.exit(1)
#    
# Reading the input DF-graph
#graph = pickle.load(open(sys.argv[1]))
graph = pickle.load(open('computed/user-file-graph'))
print 'nodes',len(graph.nodes()),graph.nodes()
print 'edges',len(graph.edges()),graph.edges()
#sys.exit(0)

score = defaultdict(float)

for node in graph.nodes():
    score[(node,node)] = 1.0

lDevelopers = []
lFiles = []

for node in graph.nodes(data=True):
    if (node[1]['type']=='Developer'): lDevelopers.append(node[0])
    else: lFiles.append(node[0])

print len(lDevelopers), lDevelopers
print len(lFiles), lFiles

print lDevelopers
print lFiles

T = 10

for iteration in range(T):
    
    flag = True
    for i in range(len(lDevelopers)):
        for j in range(i+1,len(lDevelopers)):
            
            c = 0.8
            count1 = len(graph.neighbors(lDevelopers[i]))
            count2 = len(graph.neighbors(lDevelopers[j])) 
            if(count1==0 or count2==0): continue
            
            num = 0.0
            den = 0.0
            for f1 in graph.neighbors(lDevelopers[i]):
                for f2 in graph.neighbors(lDevelopers[j]):
                    den += graph.get_edge_data(lDevelopers[i],f1)['w']* graph.get_edge_data(lDevelopers[j],f2)['w']
                    num += graph.get_edge_data(lDevelopers[i],f1)['w']* graph.get_edge_data(lDevelopers[j],f2)['w']*score[(f1,f2)]
            
            newScore = float(c*num)/float(den)
            if (score[(lDevelopers[i],lDevelopers[j])]!=newScore):
                score[(lDevelopers[i],lDevelopers[j])]=newScore
                flag=False
                
    
    for i in range(len(lFiles)):
        for j in range(i+1,len(lFiles)):
            
            c = 0.8
            count1 = len(graph.neighbors(lFiles[i]))
            count2 = len(graph.neighbors(lFiles[j]))
            if(count1==0 or count2==0): continue
            
            num = 0.0
            den = 0.0
            for d1 in graph.neighbors(lFiles[i]):
                for d2 in graph.neighbors(lFiles[j]):
                    den += graph.get_edge_data(lFiles[i],d1)['w']* graph.get_edge_data(lFiles[j],d2)['w']
                    num += graph.get_edge_data(lFiles[i],d1)['w']* graph.get_edge_data(lFiles[j],d2)['w']*score[(d1,d2)]
            
            newScore = float(c*num)/float(den)
            if (score[(lFiles[i],lFiles[j])]!=newScore):
                score[(lFiles[i],lFiles[j])]=newScore
                flag=False
            
    if(flag):
        print 'Convergence in ', iteration, 'iterations\n'
        break

for i in range(len(lDevelopers)):
    for j in range(i+1,len(lDevelopers)):
        print (lDevelopers[i],lDevelopers[j]), '--->', score[(lDevelopers[i],lDevelopers[j])]
    
for i in range(len(lFiles)):
    for j in range(i+1,len(lFiles)):
        print (lFiles[i],lFiles[j]), '--->', score[(lFiles[i],lFiles[j])]
    
pickle.dump(score, open('SimRank_scores.txt', 'w'))

