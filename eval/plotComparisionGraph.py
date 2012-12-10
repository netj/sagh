#!/usr/bin/env python
import pickle
import operator
import sys,re
from collections import defaultdict
import matplotlib.pyplot as plt

metrics = {}

title = sys.argv[1]
for filename in sys.argv[2:]:
    name = filename #.replace("scored.top-similar.", "").replace("user-user-", "")
    name = re.sub("^.*\\.user-user-(.+-(cosine_distance|distance))", "\\1", name)
    m = pickle.load(open(filename))
    for agg,data in m.iteritems():
        if agg != "average": continue # XXX only average
        metrics[(name,agg)] = data 

#epsilon = 0.01
#keys = map(lambda line: line.rstrip(), open("wellConnectedContributors-hideg"))[-50:]
keys = [i for i in data.keys()] # if not all(map(lambda data: data[i] < epsilon, metrics.values()))]
for i,k in enumerate(keys):
    print "%d\t%s" % (i, k)

# plotting difference to the baseline
baselineKey = filter(lambda (name,agg): "common-files" in name, metrics.keys())[0]
try:
    baseline = metrics[baselineKey]
except:
    baseline = metrics.values()[0]
#del metrics[baselineKey]
for key,data in metrics.iteritems():
    for i in data.keys():
        data[i] = baseline[i] - data[i]

sortingkey = lambda xs: -sum(xs) # (+max(xs)) #, max(abs(x) for x in xs), -sum(xs))
keys = sorted(keys, key=lambda i: sortingkey([data[i] for data in metrics.values()]))
#keys = sorted(keys)

#sortingColumn = sorted(metrics.keys())[0]
#keys = sorted(keys, key=lambda i: -sum(data[i] for data in [metrics[sortingColumn]]))

fig = plt.figure()
labels = []
for key in sorted(metrics.keys()):
    (name,agg) = key
    data = metrics[key]
    label = "%s (%s)" % (name,agg)
    #print data
    plt.plot(map(lambda k: data[k], keys),
            's-' if "common-files" in name else
            'o-' if "cosine" in name else '^-',
            label=label)
    labels.append(label)

plt.axhline(0, color='k', linewidth=1)
plt.xlabel('user')
plt.ylabel('Value of Metric')
plt.legend(labels, prop={"size":6})
plt.title(title)
fig.set_size_inches(8, 6)
#plt.legend(('Cosine Similarity','Average Distance'))
fig.savefig(title + ".pdf", dpi=120)
#plt.show()
plt.close()
