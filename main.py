from user import *

users = get_users()
example_user = users[0]

print("Name, id:", example_user.name, example_user.id)
print("Printing friends")
for friend in example_user.friends:
    print("friend:", friend.name)
