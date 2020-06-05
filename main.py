from user import *
from random import choice

users = get_users()
example_user = choice(users)

print("Name, id:", example_user.name, example_user.id)
print("Printing friends")
for friend in example_user.friends:
    print("friend:", friend)
