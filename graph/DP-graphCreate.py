#!/usr/bin/env python
'''
Input: Commit Log File
Output: List of (not-unique, to capture weights) Developers in memberDevelopers.txt
'''

import networkx as nx
from collections import defaultdict
import pickle
import sys

for line in sys.stdin:
    if 'Author' in line:
       
        start = line.find(':')+2
        end = line.find('<', start)
        author_name = line[start:end]
        
        start = line.find('<')+1
        end = line.find('>', start)
        author_id = line[start:end]
        
        print author_id + ',' + author_name

