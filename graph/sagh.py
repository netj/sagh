import networkx as nx
import os

currentRepo = None

def for_each_repo(job, **args):
    global currentRepo
    for repoline in file("repos.txt"):
        repo = repoline.strip()
        if len(repo) > 0 and os.path.exists("github/%s" % repo):
            currentRepo = repo
            job(repo, **args)

def fileFor(attrName):
    return "github/%s/%s" % (currentRepo, attrName)

