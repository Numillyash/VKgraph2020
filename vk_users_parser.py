from user import *
import json
from urllib.request import urlopen


include_outside_friends = False  # рассматриваются ли также друзья участников группы


# главная функция
def parse_and_save_users():
    member_ids, outside_friends = get_member_ids()
    user_data_list = get_user_data(member_ids)
    member_ids = set(member_ids)
    user_list = create_users(member_ids, user_data_list, outside_friends)
    save_to_file(user_list)


# получить id участников группы
def get_member_ids():
    member_ids = []
    
    while True:
        group_data = vkapi_get_data("groups.getMembers", group_id="fml239", offset=len(member_ids), count=1000)
        member_ids += group_data["items"]
    
        if len(member_ids) == group_data["count"]:
            break

    print("Group members ids loaded")

    outside_friends = set()
    if include_outside_friends:  # добавляем в группу также друзей участников группы
        progress_cnt = 0

        for id in member_ids:
            outside_friends.update(get_friends_ids(id))
            progress_cnt += 1
            if progress_cnt % 100 == 0:
                print("Included outside friends for", progress_cnt)

        for id in member_ids:
            outside_friends.discard(id)

        member_ids = list(set(member_ids).union(outside_friends))

    return member_ids, outside_friends


# получить информацию об участниках группы
def get_user_data(member_ids):
    user_data_list = []
    user_data_iteration = 250
    for i in range(0, len(member_ids), user_data_iteration):
        request_str = ",".join(map(str, member_ids[i : i + user_data_iteration]))
        user_data_list += vkapi_get_data("users.get", user_ids=request_str)
    
        if len(user_data_list) % 1000 == 0:
            print(f"Loaded {len(user_data_list)} user names")
    
    print("User names have been loaded")
    return user_data_list


# создать объекты класса user
def create_users(member_ids, user_data_list, outside_friends):
    user_list = []
    user_by_id = {}
    
    for user_data in user_data_list:
        user_id = user_data["id"]
        if "deactivated" in user_data:
            member_ids.remove(user_id)
            outside_friends.discard(user_id)
            continue
    
        user_name = user_data["first_name"] + " " + user_data["last_name"]
        user_name = user_name.replace(",", "")
        is_closed = user_data["is_closed"]
        new_user = User(user_id, user_name, is_closed)
        user_list.append(new_user)
        user_by_id[new_user.id] = new_user
        if len(user_list) % 10000 == 0:
            print(f"Created {len(user_list)} users")

    # загружаем друзей пользователей
    friends_loaded = 0
    for user in user_list:
        if user.is_closed:
            continue
        if user.id in outside_friends:
            continue
        friends_ids = get_friends_ids(user.id)
        # загружаем друзей только из группы
        user._friends_ids = [id for id in friends_ids if id in member_ids]
        friends_loaded += 1
        if friends_loaded % 100 == 0:
            print(f"Loaded friends for {friends_loaded} users")
    print("Total friends loaded:", friends_loaded)
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
