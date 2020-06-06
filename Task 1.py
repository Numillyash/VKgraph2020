from user import *
from itertools import combinations
from collections import defaultdict
from random import random
import matplotlib.pyplot as plt
import numpy as np
import math
users = get_users()
#example_user = users[0]

#print("Name, id:", example_user.name, example_user.id)
#print("Printing friends")
#for friend in example_user.friends:
#    print("friend:", friend.name)

count_vert = len(users)
count_rebri = 0
for user in users:
    for friend in user.friends:
        count_rebri += 0.5

print("Всего вершин: ",count_vert, ", всего ребер: ",int(count_rebri),  ", Отношение: ",count_vert/count_rebri)

names = []
kolvos = []

for i in users:
    kolvos.append(len(i.friends))
    names.append(i.name)

d = {names[i]: kolvos[i] for i in range(len(kolvos))}

itog_list = sorted(d, key=d.get, reverse=True)
ans = [itog_list[i] for i in range(20)]
print(ans)
rng = np.arange(1001)

xAxe = rng / 1000
aller = xAxe*5
fig, ax = plt.subplots(figsize=(5, 3))
ax.stackplot(xAxe, aller)
ax.set_title('Вероятность ребра')
ax.legend(loc='upper left')
ax.set_ylabel('Вероятность связности')
ax.set_xlim(xmin=xAxe[0], xmax=xAxe[-1])
fig.tight_layout()

plt.show()