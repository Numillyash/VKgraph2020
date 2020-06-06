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
        return f"Name: {self.name}"

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


_users_list = None
_index_of_user = None
_users_by_id = None


# возвращает список всех пользователей
def get_users():
    global _users_list, _index_of_user, _users_by_id

    if _users_list is None:
        file = open("users.dat", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        _users_list = []
        _users_by_id = {}
        _index_of_user = {}
        users_amount = int(lines[0])

        for i in range(1, users_amount + 1):
            new_user = User()
            new_user._load(lines[i])
            _users_list.append(new_user)
            _users_by_id[new_user.id] = new_user
            _index_of_user[new_user] = i - 1

        for user in _users_list:
            user.friends = set([_users_by_id[id] for id in user._friends_ids])
            del user._friends_ids
    return _users_list


# возвращает юзера по id вконтакте
def get_user_by_id(id):
    return _users_by_id[id]


# возращает юзера по имени вконтакте
def get_user_by_name(name):
    if _users_list is None:
        get_users()

    for user in _users_list:
        if user.name == name:
            return user


# возвращает индекс юзера в массиве users
def get_index_of_user(user):
    return _index_of_user[user]