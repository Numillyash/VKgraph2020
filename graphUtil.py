import networkx
import time
import collections
import graphviz
from networkx.drawing.nx_agraph import graphviz_layout
from user import *
from graph_tools import Graph


graph = {}
users_n = get_users()
users = [users_n[i] for i in range(100)]

for user in users:
    graph[user.id] = [i.id for i in user.friends]
#print(graph)
g=Graph()

for i in graph:
    g.add_vertex(i)
    #print(i, g)
    for j in graph[i]:
        #print(j)
        if i != j and i in graph and j in graph:
            #print("doner")
            g.add_edge(i, j)
#print(g.edges())
g.draw('file.png', prog = "circo")
