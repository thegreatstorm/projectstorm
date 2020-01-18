import random
import socket


def random_port():
    port = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        port = random.randint(28000, 50000)
        result = sock.connect_ex(('127.0.0.1', port))
        if result != 0:
            break

    sock.close()

    return port
