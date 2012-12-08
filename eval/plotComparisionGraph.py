#!/usr/bin/env python
import pickle
import operator
import sys,re
from collections import defaultdict
import matplotlib.pyplot as plt

metrics = {}

title = sys.argv[1]
for filename in sys.argv[2:]:
    name = filename.replace("scored.top-similar."+title+".", "").replace("user-user-", "")
    name = re.sub("^\\d+.", "", name)
    m = pickle.load(open(filename))
    for agg,data in m.iteritems():
        if agg != "average": continue
        metrics[(name,agg)] = data 

keys = data.keys()
for i,k in enumerate(keys):
    print "%d\t%s" % (i, k)


plt.figure()
labels = []
for key in sorted(metrics.keys()):
    (name,agg) = key
    data = metrics[key]
    label = "%s (%s)" % (name,agg)
    #print data
    plt.plot(map(lambda k: data[k], keys),
            'o-' if "cosine" in name else '^-',
            label=label)
    labels.append(label)
plt.xlabel('user')
plt.ylabel('Value of Metric')
plt.legend(labels)
plt.title(title)
#plt.legend(('Cosine Similarity','Average Distance'))
plt.savefig(title + ".pdf")
plt.show()
plt.close()
