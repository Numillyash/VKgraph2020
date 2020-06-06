import networkx
import time
import collections
import graphviz
from networkx.drawing.nx_agraph import graphviz_layout
from user import *
import pygraphviz as pgv


graph = {}
users_n = get_users()
users = [users_n[i] for i in range(100)]

for user in users:
    graph[user.id] = [i.id for i in user.friends]
#print(graph)
g=pgv.AGraph()

for i in graph:
    g.add_node(i)
    #print(i, g)
    for j in graph[i]:
        #print(j)
        if i != j and i in graph and j in graph:
            #print("doner")
            g.add_edge(i, j)
#print(g.edges())
#cool g.draw('file.png', prog = "circo")
g.draw('file.png', prog = "twopi")
