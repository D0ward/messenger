from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = '0.0.0.0'
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_connections():
    while True:
        client, client_addr = SERVER.accept()
        print('CONNECTED:', client_addr)
        client.send(bytes("Write your name: ", "utf8"))

        addresses[client] = client_addr
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZE).decode("utf8")
    
    welcome = f'Welcome {name}! Write (quit) to leave.'
    client.send(bytes(welcome, "utf8"))
    broadcast(bytes(f'{name} joined', "utf8"))

    clients[client] = name

    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes("(quit)", "utf8"):
            broadcast(msg, name + ': ')
        else:
            client.send(bytes("(quit)", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} leave.", "utf8"))
            break


def broadcast(message, prefix = ''):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)

if __name__ == "__main__":
    SERVER.listen(2)
    print("Wait connections")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()  
    ACCEPT_THREAD.join()
    SERVER.close()
