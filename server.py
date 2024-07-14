from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from encryption import create_public_keys

clients = []
friend = {}

HOST = '0.0.0.0'
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def send(client: socket, message: str, id = '003'):
    client.send(bytes(id + ' ' + message, "utf8"))

def start_encryption(client: socket):

    public_key1, public_key2 = create_public_keys()
    send(client, str(public_key1) + ' ' + str(public_key2), '001')
    send(friend[client], str(public_key1) + ' ' + str(public_key2), '001')
    

def accept_connections():
    while True:
        client, client_addr = SERVER.accept()
        print('CONNECTED:', client_addr)
        send(client, "Write your name: ")

        
        clients.append(client)
        
        Thread(target=handle_client, args=(client,)).start()

def registration(client: socket, name: str):
    send(client, f'Welcome {name}! Write (quit) to leave.')
    

    if len(clients) == 2:
            friend[client] = clients[0]
            friend[clients[0]] = client
            send(friend[client], f'{name} is online', "003")
            start_encryption(client)
    
cnt_ready = 0
def handle_client(client: socket):
    global cnt_ready
    name = ''
    
    while True:
        id, *msg = client.recv(BUFSIZE).decode("utf8").split()
        msg = ' '.join(msg)
        print(id, msg)
        
        match id:
            case '000':
                name = msg
                registration(client, name)
            case '011':
                cnt_ready += 1
                if cnt_ready == 2:
                    send(client, '', '011')
                    send(friend[client], '', '011')
            case '002':
                partial_key = msg
                send(friend[client], partial_key, '002')
            case '003':
                send(friend[client], name + ':' + msg, '003')
                send(client, name + ':' + msg, '003')
            case '005':
                client.send(bytes("(quit)", "utf8"))
                client.close()
                del clients[client]
                
                send(friend[client], name + 'leave', '003')
                send(client, name + 'leave' '003')
                break
            

if __name__ == "__main__":
    SERVER.listen(2)
    print("Wait connections")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()  
    ACCEPT_THREAD.join()
    SERVER.close()
