from igraph import *
from user import *


def get_graph():
    users = get_users()
    index_of_user = {}
    for i in range(len(users)):
        index_of_user[users[i].id] = i

    g = Graph()
    g.add_vertices(len(users))

    edges = []
    for user in users:
        for friend in user.friends:
            edges.append((index_of_user[user.id], index_of_user[friend.id]))

    g.add_edges(edges)
    return g

