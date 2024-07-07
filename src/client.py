#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import encryption


'''
id message

000 registration user
001 get public keys
002 swap partial keys
003 message
004 choose user
005 leave user
'''
on_encrypt = False

def send_server(server: socket, message: str, id = '003'):
    server.send(bytes(id + ' ' + message, "utf8"))

def set_keys(public_key1: int, public_key2: int) -> None:
    encrypt.set_public_keys(public_key1, public_key2)

def unable_encryption() -> None:
    global id, on_encrypt
    id = '003'
    on_encrypt = True

def receive():
    global on_encrypt, encrypt

    while True:
        try:
            id, *msg = client_socket.recv(BUFSIZE).decode("utf8").split()
            print(id, msg)
            
            match id:
                case '001': #get public keys and send partial_key
                    msg_list.insert(tkinter.END, "gets public keys, please wait")
                    public_key1 = int(msg[0])
                    public_key2 = int(msg[1])
                    set_keys(public_key1, public_key2)
                    send_server(client_socket, '', '011')
                case '011':
                    send_server(client_socket, str(encrypt.create_partial_key()), '002')
                case '002': 
                    msg_list.insert(tkinter.END, "create full keys, please wait")
                    partial_key = int(msg[0])
                    encrypt.create_full_key(partial_key)
                    msg_list.insert(tkinter.END, "done")
                    unable_encryption()
                case '003':
                    if on_encrypt:
                        msg = ''.join(msg)
                        name, *msg = msg.split(':')
                        msg = ''.join(msg)
                        msg = name + ': ' + encrypt.decrypt_message(msg)
                        
                    msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    global id, on_encrypt, encrypt
    print(id)
    msg = my_msg.get()
    my_msg.set("")

    if msg == "(quit)":
        id = '005'
    if on_encrypt:
        msg = encrypt.encrypt_message(''.join(msg))
    send_server(client_socket, msg, id)

    if msg == "(quit)":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("(quit)")
    send()


id = '000'
top = tkinter.Tk()
top.title("TkMessenger")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Write your message this")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


HOST = input('Write host: ')
PORT = input('Write port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZE = 1024
ADDR = (HOST, PORT)

encrypt = encryption.Encryption()

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
