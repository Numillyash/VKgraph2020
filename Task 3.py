# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from igraph_util import *

users = get_users()
clusters = get_clusters()
print("length of clusters:", len(clusters))

#target_user = get_user_by_name("Vsevolod Lavrov")  # 11-1 класс и матцентр 11 класса
target_user = get_user_by_name("Daniil Grinchenko")  # параллель 10-х классов
#target_user = get_user_by_name("Roman Mikhaylov")  # часть 10-1 класса
#target_user = get_user_by_name("Lev Leontyev")  # oops

for cluster in clusters:
    if target_user in cluster:
        print("size of cluster:", len(cluster))
        for user in cluster:
            print(user.name)
