# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from igraph_util import *

users = get_users()
clusters = get_clusters()
print("Количество классов:", len(clusters))

answer = input("Введите id пользователя, либо имя и фамилию")
if answer.isdigit():
    target_user = get_user_by_id(int(answer))
else:
    target_user = get_user_by_name(answer)

#target_user = get_user_by_name("Георгий Улановский")  # 10-4 класс
#target_user = get_user_by_name("Роман Михайлов")  # часть 10-1 класса
#target_user = get_user_by_name("Даниил Гринченко")  # ещё параллель 10-х классов
#target_user = get_user_by_name("Всеволод Лавров")  # 11-1 класс и матцентр 11 класса
#target_user = get_user_by_name("Лев Леонтьев")  # oops

for cluster in clusters:
    if target_user in cluster:
        print("Размер текущего класса:", len(cluster))
        for user in cluster:
            print(user.name)
