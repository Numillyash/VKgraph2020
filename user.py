# обьект класса User имеет:
#   Поле name
#   Поле id
#   Поле friends (set друзей)
#   Поле is_closed (закрыта ли страница)

# Модуль user имеет функции:
#   get_users()
#   get_user_by_id(int)
#   get_user_by_name(string)
#   get_index_of_user(User)

class User:
    def __init__(self, id=None, name=None, is_closed=False):
        self.id = id
        self.name = name
        self.is_closed = is_closed
        self.friends = set()
        self._friends_ids = []

    def __str__(self):
        return self.name

    def __hash__(self):
        return id(self)

    def _save(self, file):
        file.write(f"{self.id},{self.name},{self.is_closed},")
        file.write(",".join(map(str, self._friends_ids)))

    def _load(self, string):
        fields = string.split(",")
        self.id = int(fields[0])
        self.name = fields[1]
        self.is_closed = bool(fields[2])
        self._friends_ids = list(map(int, fields[3:-1]))


# для каждой переменной есть две версии: без внешних друзей, и с внешними друзьями
_users_list = [None, None]
_index_of_user = [None, None]
_users_by_id = [None, None]


# возвращает список всех пользователей
def get_users(include_outside_friends=False):
    global _users_list, _index_of_user, _users_by_id
    index = int(include_outside_friends)

    if _users_list[index] is None:
        filename = "users_with_outside_friends.dat" if include_outside_friends else "users.dat"
        file = open(filename, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        users_list = []
        users_by_id = {}
        index_of_user = {}
        users_amount = int(lines[0])

        for i in range(1, users_amount + 1):
            new_user = User()
            new_user._load(lines[i])
            users_list.append(new_user)
            users_by_id[new_user.id] = new_user
            index_of_user[new_user] = i - 1

        for user in users_list:
            user.friends = set(users_by_id[id] for id in user._friends_ids)
            del user._friends_ids

        _users_list[index] = users_list
        _users_by_id[index] = users_by_id
        _index_of_user[index] = index_of_user

    return _users_list


# возвращает юзера по id вконтакте
def get_user_by_id(id, include_outside_friends=False):
    index = int(include_outside_friends)
    if _users_list[index] is None:
        get_users(include_outside_friends)

    return _users_by_id[int(include_outside_friends)][id]


# возращает юзера по имени вконтакте
def get_user_by_name(name, include_outside_friends=False):
    index = int(include_outside_friends)
    if _users_list[index] is None:
        get_users()

    for user in _users_list[index]:
        if user.name == name:
            return user

    raise NameError(f"Name {name} is incorrect, or the person is not in FML 239 group")


# возвращает индекс юзера в массиве users
def get_index_of_user(user, include_outside_friends=False):
    return _index_of_user[int(include_outside_friends)][user]