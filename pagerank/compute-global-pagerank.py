#!/usr/bin/env python
import networkx as nx
import sagh
import re

g = nx.Graph()

# load subgraphs into a global graph
def loadSubgraph(repo):
    g.add_node(repo, type="project")
    totalWeight = 0
    for line in file(sagh.fileFor("contributors.txt")):
        columns = re.split("\t", line)
        weight = float(columns[1])
        totalWeight += weight
    for line in file(sagh.fileFor("contributors.txt")):
        columns = re.split("\t", line)
        email = columns[0]
        weight = float(columns[1]) / totalWeight
        g.add_edge(email, repo, weight=weight)
sagh.for_each_repo(loadSubgraph)

dg = g.to_directed()

# run pagerank
pagerank = nx.pagerank(dg, max_iter=1000, weight="weight")

# output
for n,pr in pagerank.iteritems():
    print n, pr, ("(%d)" if "type" in g.node[n] else "%d") % len(g.neighbors(n))


## summary
#projectPagerank = {}
#developerPagerank = {}
#for n,v in pagerank.iteritems():
#    if "type" in g.node[n]:
#        pr = projectPagerank
#    else:
#        pr = developerPagerank
#    pr[n] = v
#
#for n,v in projectPagerank.iteritems():
#    print n,v
#print "min/max"
#print min(projectPagerank.values()), max(projectPagerank.values())
#print min(developerPagerank.values()), max(developerPagerank.values())
