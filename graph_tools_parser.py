from graph_tools import Graph
from user import *

def get_graph():
    g = Graph(directed=False)
    users = get_users()
    for user in users:
        for friend in user.friends:
            g.add_edge(user.id, friend.id)
