# Привет, это туториал по user
from user import *  # импорт с файла user.py

users = get_users(False)  # получаем список юзеров
# параметр True - также учитывать друзей участников группы
example_user = get_user_by_id(6)  # выбираем юзера

print("Name, id:", example_user.name, example_user.id)
print("Printing friends")
for friend in example_user.friends:
    print("friend:", friend.name)

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