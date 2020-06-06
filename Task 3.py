from igraph_util import *
import louvain

users = get_users()
g = get_graph()
clustering = louvain.find_partition(g, louvain.CPMVertexPartition)
print(len(clustering), "clusters")

#target_index = get_index_of_user(get_user_by_name("Vsevolod Lavrov"))
target_index = get_index_of_user(get_user_by_name("Daniil Grinchenko"))

for cluster in clustering:
    if target_index in cluster:
        print("len of cluster:", len(cluster))
        for id in cluster:
            print(users[id])
        print()
