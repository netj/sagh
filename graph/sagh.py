import networkx as nx
import os

currentRepo = None

def for_each_repo(job, **args):
    global currentRepo
    for repoline in file("repos.txt"):
        repo = repoline.strip()
        if len(repo) > 0 and os.path.exists("computed/%s" % repo):
            currentRepo = repo
            try:
                job(repo, **args)
            except:
                True

def fileFor(attrName):
    global currentRepo
    filename = "computed/%s/%s" % (currentRepo, attrName)
    if os.path.exists(filename):
        return filename
    else:
        raise Exception("%s: Not found" % filename)

