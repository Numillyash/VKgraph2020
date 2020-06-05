import pickle


class User:
    def __init__(self, id=None, name=None, is_closed=False):
        self.id = id
        self.name = name
        self.is_closed = is_closed
        self.friends = set()  # список друзей (классы user)

    def __str__(self):
        return f"Id: {self.id}, Name: {self.name}"

    def __hash__(self):
        return id(self)


_users_list = None


# возращает массив всех пользователей
def get_users():
    global _users_list

    if _users_list is None:
        file = open("users.dat", "rb")
        _users_list = pickle.load(file)
        file.close()

    return _users_list
