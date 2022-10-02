# coding: UTF-8
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# CONSTANTS
HOST = '127.0.0.1'
PORT = 33000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# GLOBALS
clients = {}
addresses = {}


def broadcast(msg, prefix=""):
    print(f'[BROADCAST] {prefix + str(msg)}')
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def handle_new_connections():
    while True:
        client, client_address = SERVER.accept()
        print(f'{client_address} se conectou.')
        client.send(bytes("Entre seu nick!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(BUFFER_SIZE).decode("utf8")
    welcome = f'Bem-vindo {name}! Se desejar sair, digite "/sair".'
    client.send(bytes(welcome, "utf8"))
    try:
        msg = "%s entrou." % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(BUFFER_SIZE)
            # Command handler
            if msg == bytes("/sair", "utf8"):
                raise Exception()

            if msg == bytes("/usuarios", "utf8"):
                users = 'Estão online: ' + ', '.join(clients.values())
                client.send(bytes(users, 'utf8'))

            # Just got a message, so broadcast to other users
            else:
                broadcast(msg, name + ": ")

    except Exception:
        broadcast(bytes("%s saiu." % name, "utf8"))

    finally:
        client.close()
        del clients[client]
        client.close()


if __name__ == "__main__":
    SERVER.listen(5)
    print("> Aguardando por conexões...")
    ACCEPT_THREAD = Thread(target=handle_new_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
