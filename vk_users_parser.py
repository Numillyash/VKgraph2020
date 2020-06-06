from user import *
import json
from urllib.request import urlopen


include_outside_friends = False  # друзья участников группы тоже рассматриваются


# главная функция
def parse_and_save_users():
    member_ids = get_member_ids()
    user_data_list = get_user_data(member_ids)
    user_list = create_users(member_ids, user_data_list)
    save_to_file(user_list)


# получить id участников группы
def get_member_ids():
    member_ids = []
    
    while True:
        group_data = vkapi_get_data("groups.getMembers", group_id="fml239", offset=len(member_ids), count=1000)
        member_ids += group_data["items"]
    
        if len(member_ids) == group_data["count"]:
            break
    
    if include_outside_friends:
        member_ids_set = set(member_ids)
        for id in member_ids:
            member_ids_set.update(get_friends_ids(id))
        member_ids = list(member_ids_set)


    return member_ids


# получить информацию об участниках группы
def get_user_data(member_ids):
    user_data_list = []
    for i in range(0, len(member_ids), 100):
        request_str = ",".join(map(str, member_ids[i : i + 100]))
        user_data_list += vkapi_get_data("users.get", user_ids=request_str)
    
        if len(user_data_list) % 500 == 0:
            print(f"Loaded {len(user_data_list)} user names")
    
    print("User names have been loaded")
    return user_data_list


# создать объекты класса user
def create_users(member_ids, user_data_list):
    user_list = []
    user_by_id = {}
    
    for user_data in user_data_list:
        user_id = user_data["id"]
        if "deactivated" in user_data:
            member_ids.remove(user_id)
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
        friends_ids = get_friends_ids(user.id)
        # загружаем друзей только из группы
        user._friends_ids = [id for id in friends_ids if id in member_ids]
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
    return user_list


# сохранить список пользователей в файл
def save_to_file(user_list):
    filename = "users_with_outside_friends.dat" if include_outside_friends else "users.dat"
    file = open(filename, "w", encoding="utf-8")
    file.write(str(len(user_list)) + "\n")

    for user in user_list:
        user._save(file)
        file.write("\n")

    file.close()


# возращает словарь с данными из vkapi
def vkapi_get_data(method, **kwargs):
    token = "b3776227b3776227b3776227fcb305108fbb377b3776227edadc2c9b6729a01af3db2fd"
    url = f"https://api.vk.com/method/{method}?access_token={token}&v=5.107&lang=ru"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    data = json.loads(urlopen(url).read())
    if "response" in data:
        return data["response"]
    else:
        return None


def get_friends_ids(user_id):
    friends_data = vkapi_get_data("friends.get", user_id=user_id)
    if friends_data:
        return friends_data["items"]
    else:  # аккаунт закрыт
        return []


if __name__ == "__main__":
    parse_and_save_users()