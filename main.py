from user import *

users = get_users()
example_user = users[0]

#print("Name, id:", example_user.name, example_user.id)
#print("Printing friends")
#for friend in example_user.friends:
#    print("friend:", friend.name)

count_vert = len(users)
count_rebri = 0
for user in users:
    for friend in user.friends:
        if user.name in (names.name for names in friend.friends):
            count_rebri += 1
        else:
            friend.friends.append(user)
            count_rebri += 1

print("Всего вершин: ",count_vert, ", всего ребер: ",int(count_rebri),  ", Отношение: ",count_vert/count_rebri)