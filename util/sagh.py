import networkx as nx
import os,sys

currentRepo = None

def for_each_repo(job, **args):
    global currentRepo
    for repoline in file("../repos.txt"):
        repo = repoline.strip()
        #print >>sys.stderr, repo
        if len(repo) > 0 and os.path.exists("%s" % repo):
            currentRepo = repo
            try:
                job(repo, **args)
            except:
                print >>sys.stderr, "%s: Error:" % repo, sys.exc_info()

def fileFor(attrName):
    global currentRepo
    filename = "%s/%s" % (currentRepo, attrName)
    if os.path.exists(filename):
        return filename
    else:
        raise Exception("%s: Not found" % filename)

def suffixWithArgs(basename='', upToNumArgs=len(sys.argv)-1):
    name = basename
    for i in range(1, min(upToNumArgs+1, len(sys.argv))):
        name += '-' + sys.argv[i]
    return name

# normalizing a vector
def normalize(d, by=sum):
    base = float(by(d.values()))
    nd = {}
    for k,v in d.iteritems():
        nd[k] = float(v)/base
    return nd
