# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from igraph_util import *

clusters = get_clusters()
print("Количество классов:", len(clusters))

answer = input("Введите id пользователя, либо имя и фамилию")
if answer.isdigit():
    target_user = get_user_by_id(int(answer))
else:
    target_user = get_user_by_name(answer)

for cluster in clusters:
    if target_user in cluster:
        print("Размер текущего класса:", len(cluster))
        for user in cluster:
            print(user.name)
