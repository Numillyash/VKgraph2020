from collections import defaultdict

from user import *


def get_degree_distribution():
    users = get_users()
    distribution = defaultdict(int)
    for user in users:
        distribution[len(user.friends)] += 1

    return distribution


if __name__ == "__main__":
    print(get_degree_distribution())