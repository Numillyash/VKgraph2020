from igraph_util import *
import  networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from user import *
import pygraphviz as pgv

def getClPhoto():
    clusters = get_clusters()
    ind = 0
    obsch = 0
    for i in clusters:
        obsch+=1
        print(obsch)
        if(len(i) >= 10):
            ind += 1
            g = pgv.AGraph(mode = "mds")
            g.node_attr.update()
            for people in i:
                if(not people.name in g.nodes()):
                    g.add_node(people.name)
            print("Done nodes")
            for people in i:
                for friend in people.friends:
                    if friend in i:
                        g.add_edge(people.name, friend.name)
            print("Done edges")
            g.draw(f"Clusters/cluster{ind}.png", prog="circo", args = "")
            print(f"End number {ind}")

getClPhoto()
print("Programm is done")