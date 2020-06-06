import leidenalg  # pip install leidenalg
from igraph import *
from user import *
from collections import defaultdict


def get_graph():
    users = get_users()

    g = Graph()
    g.add_vertices(len(users))

    edges = []
    for user in users:
        for friend in user.friends:
            edges.append((get_index_of_user(user), get_index_of_user(friend)))

    g.add_edges(edges)
    return g


def get_degree_distribution():
    users = get_users()
    distribution = defaultdict(int)
    for user in users:
        distribution[len(user.friends)] += 1

    return distribution

# возвращает список кластеров. Каждый кластер - список юзеров
def get_clusters():
    users = get_users()
    g = get_graph()

    clustering = leidenalg.find_partition(g, leidenalg.CPMVertexPartition)
    user_clusters = [set(users[index] for index in cluster) for cluster in clustering]
    return user_clusters
