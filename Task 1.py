from user import *
from itertools import combinations
from collections import defaultdict
from random import random
import matplotlib.pyplot as plt
import numpy as np
import math
from igraph_util import *
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
print(", ".join(ans))

dabs = get_degree_distribution()

s = dict(sorted(dabs.items()))

keys = list(s.keys())
keys.pop(0)
values = list(s.values())
values.pop(0)

x_val = [i for i in range(1,1000)]
y_val = [5115.49697848*(x**-1.502028) for x in x_val]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(keys, values, label="Значения")
ax.plot(x_val, y_val, c='red', label="Степенная функция\nf(x)=5115.497*x^-1.502")
ax.set_title('Гистограмма кол-ва друзей')
ax.set_ylabel('Кол-во людей')
ax.set_xlabel('Кол-во друзей')
ax.set_xlim(xmin=keys[0], xmax=300)#keys[-1])
ax.set_ylim(ymin=values[-1], ymax=500)#values[0])
ax.legend()

fig.tight_layout()
plt.savefig('Gist.png', format='png', dpi=1000)
plt.show()