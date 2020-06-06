# Обьект класса User имеет:
#   Поле name
#   Поле id
#   Поле friends (set друзей)
#   Поле is_closed (закрыта ли страница)

class User:
    def __init__(self, id=None, name=None, is_closed=False):
        self.id = id
        self.name = name
        self.is_closed = is_closed
        self.friends = set()  # список друзей (классы user)
        self._friends_ids = []

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}"

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


# возращает массив всех пользователей
def get_users():
    global _users_list

    if _users_list is None:
        file = open("users.dat", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        _users_list = []
        users_by_id = {}
        users_amount = int(lines[0])

        for i in range(1, users_amount + 1):
            new_user = User()
            new_user._load(lines[i])
            _users_list.append(new_user)
            users_by_id[new_user.id] = new_user

        for user in _users_list:
            user.friends = set([users_by_id[id] for id in user._friends_ids])
            del user._friends_ids
    return _users_list
