from user import *
import json
from urllib.request import urlopen


# возращает словарь с данными из vkapi
def vkapi_get_data(method, **kwargs):
    token = "b3776227b3776227b3776227fcb305108fbb377b3776227edadc2c9b6729a01af3db2fd"
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
user_list = []
user_by_id = {}

for user_data in user_data_list:
    user_id = user_data["id"]
    if "deactivated" in user_data:
        members_ids.remove(user_id)
        continue

    user_name = user_data["first_name"] + " " + user_data["last_name"]
    user_name = user_name.replace(",", "")
    is_closed = user_data["is_closed"]
    new_user = User(user_id, user_name, is_closed)
    user_list.append(new_user)
    user_by_id[new_user.id] = new_user

# загружаем друзей пользователей
friends_loaded = 0
for user in user_list:
    if user.is_closed:
        continue
    friends_data = vkapi_get_data("friends.get", user_id=user.id)
    friends_ids = friends_data["items"]
    # загружаем друзей только из группы
    user._friends_ids = [id for id in friends_ids if id in members_ids]
    friends_loaded += 1
    if friends_loaded % 100 == 0:
        print(f"Loaded friends for {friends_loaded} users")


# проверяем, что всегда есть обратное ребро
for user in user_list:
    for friend_id in user._friends_ids:
        friend = user_by_id[friend_id]
        if user.id not in friend._friends_ids:
            friend._friends_ids.append(user.id)

print("User loading successful!")

# сохраняем список пользователей в файл
file = open("users.dat", "w", encoding="utf-8")
file.write(str(len(user_list)) + "\n")

for user in user_list:
    user._save(file)
    file.write("\n")

file.close()
