# Task 3. Попробовать выделить классы (почти полные подграфы графа дружбы).
from user import *
import sys

sys.setrecursionlimit(10 ** 9)

users = get_users()

n = min(len(users), 1000)
class_number = [-1] * n
classes_graph = [[] for i in range(n)]

# 2 пользователя, у которых >= x общих друзей, принадлежат одному классу
for i in range(n):
    for j in range(i + 1, n):
        user1 = users[i]
        user2 = users[j]
        if user2 not in user1.friends:
            continue
        common_friends = set(user1.friends).intersection(set(user2.friends))
        if len(common_friends) >= 10:
            classes_graph[i].append(j)
            classes_graph[j].append(i)

print("Done!")


def dfs(v):
    for w in classes_graph[v]:
        if class_number[w] != class_number[v]:
            class_number[w] = class_number[v]
            dfs(w)


classes_amount = 0
for i in range(n):
    if class_number[i] != -1:  # вершина не принадлежит ни одному классу - добавляем ещё один
        continue
    classes_amount += 1
    class_number[i] = classes_amount
    dfs(i)

print("classes amount:", classes_amount)
print("desired amount:", n / 30)
