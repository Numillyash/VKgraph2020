import sys

from user import *
import json
from urllib.request import urlopen
import pickle


# возращает словарь с данными из vkapi
def vkapi_get_data(method, **kwargs):
    token = "ae05dc6dae05dc6dae05dc6dc9ae77b337aae05ae05dc6df0dffc2a3f8bde9fa2172d79"
    url = f"https://api.vk.com/method/{method}?access_token={token}&v=5.107"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    data = json.loads(urlopen(url).read())
    return data["response"]


# получаем id и имена участников группы
members_ids = []
user_data_list = []

while True:
    group_data = vkapi_get_data("groups.getMembers", group_id="fml239", offset=len(members_ids), count=100)
    members_ids += group_data["items"]

    request_str = ",".join(map(str, group_data["items"]))
    user_data_list += vkapi_get_data("users.get", user_ids=request_str)

    if len(members_ids) % 500 == 0:
        print(f"Loaded {len(members_ids)} user names")

    if len(members_ids) == group_data["count"]:
        break

print("User names have been loaded")


# создаем объекты класса user
users_by_id = {}
user_list = []

for user_data in user_data_list:
    user_id = user_data["id"]
    if "deactivated" in user_data:
        members_ids.remove(user_id)
        continue

    user_name = user_data["first_name"] + " " + user_data["last_name"]
    is_closed = user_data["is_closed"]
    new_user = User(user_id, user_name, is_closed)

    users_by_id[new_user.id] = new_user
    user_list.append(new_user)


# загружаем друзей пользователей
friends_loaded = 0
for user in user_list:
    if user.is_closed:
        continue
    friends_data = vkapi_get_data("friends.get", user_id=user.id)
    friends_ids = friends_data["items"]
    # загружаем друзей только из группы
    user.friends = set([users_by_id[id] for id in friends_ids if id in members_ids])

    friends_loaded += 1
    if friends_loaded % 100 == 0:
        print(f"Loaded friends for {friends_loaded} users")


# проверяем, что всегда есть обратное ребро
for user in user_list:
    for friend in user.friends:
        if not (user.id in (ids.id for ids in friend.friends)):
            friend.friends.add(user)

print("User loading successful!")

# сохраняем список пользователей в файл
sys.setrecursionlimit(10 ** 9)
file = open("users.dat", "wb")
pickle.dump(user_list, file)
file.close()
