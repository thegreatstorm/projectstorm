import random

def random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password_length = 8
    new_password = "".join(random.sample(s, password_length))
    return new_password

# print(get_password())