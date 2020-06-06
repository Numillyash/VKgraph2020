# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from igraph_util import *

users = get_users()
clusters = get_clusters()
print("Количество кластеров:", len(clusters))

answer = input("Введите id пользователя, либо имя и фамилию латиницей: ")
if answer.isdigit():
    target_user = get_user_by_id(int(answer))
else:
    target_user = get_user_by_name(name)

#target_user = get_user_by_name("Georgy Ulanovsky")  # 10-4 класс
#target_user = get_user_by_name("Roman Mikhaylov")  # часть 10-1 класса
#target_user = get_user_by_name("Daniil Grinchenko")  # ещё параллель 10-х классов
#target_user = get_user_by_name("Vsevolod Lavrov")  # 11-1 класс и матцентр 11 класса
#target_user = get_user_by_name("Lev Leontyev")  # oops

for cluster in clusters:
    if target_user in cluster:
        print("Размер текущего кластера:", len(cluster))
        for user in cluster:
            print(user.name)
