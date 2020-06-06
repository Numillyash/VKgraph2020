# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from collections import defaultdict

from user import *

users = get_users()

# используем алгоритм СНМ (система непересекающихся множеств, https://e-maxx.ru/algo/dsu)
n = len(users)
parent = [i for i in range(n)]
classes_amount = n  # изначально каждый в классе из 1 человека


def find_class(v):
    if parent[v] == v:
        return v
    else:
        parent[v] = find_class(parent[v])
        return parent[v]


def union_classes(a, b):
    a = find_class(a)
    b = find_class(b)
    if a != b:
        parent[b] = a
        global classes_amount
        classes_amount -= 1


# 2 знакомых пользователя, у которых >= x общих друзей, принадлежат одному классу
for i in range(n):
    for j in range(i + 1, n):
        if find_class(i) == find_class(j):  # они уже в 1 классе
            continue

        user1 = users[i]
        user2 = users[j]

        if user2 in user1.friends:
            common_friends = user1.friends.intersection(user2.friends)
            if len(common_friends) >= 40:
                union_classes(i, j)
                if classes_amount % 100 == 0:
                    print("now it's", classes_amount)

classes = defaultdict(set)

for i in range(n):
    classes[find_class(i)].add(i)

print("classes amount:", classes_amount, "n / 30:", n / 30)
for class_list in classes.values():
    if len(class_list) >= 5:
        print([str(users[index]) for index in class_list])
