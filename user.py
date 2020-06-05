import pickle


class User:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        self.friends = []  # список друзей (классы user)

    def __str__(self):
        return f"Id: {self.id}, name: {self.name}"

users_list = None


# возращает массив всех пользователей
def get_users():
    global users_list

    if users_list is None:
        file = open("users.dat", "rb")
        users_list = pickle.load(file)
        file.close()

    return users_list
