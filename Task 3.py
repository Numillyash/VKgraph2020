from igraph_util import *
import leidenalg   # pip install leidenalg

users = get_users()
g = get_graph()
clustering = leidenalg.find_partition(g, leidenalg.CPMVertexPartition)
print(len(clustering), "clusters")

target_index = get_index_of_user(get_user_by_name("Vsevolod Lavrov"))  # 11-1 класс и матцентр 11 класса
#target_index = get_index_of_user(get_user_by_name("Daniil Grinchenko"))  # параллель 10-х классов

for cluster in clustering:
    if target_index in cluster:
        print("len of cluster:", len(cluster))
        for id in cluster:
            print(users[id])
        print()
