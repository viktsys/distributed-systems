from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import Tk, Frame, StringVar, Listbox, Entry, Button, Scrollbar
from tkinter import (
    X as TK_X, Y as TK_Y,
    LEFT as TK_LEFT, RIGHT as TK_RIGHT,
    BOTH as TK_BOTH, END as TK_END,
)


def receive_message():
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            messages_list.insert(TK_END, msg)
        except OSError:
            break


def send_message(event=None):
    msg_content = msg.get()
    msg.set("")
    client_socket.send(bytes(msg_content, "utf8"))

    # If is a /sair command, drop the socket and quit
    if msg == "/sair":
        client_socket.close()
        window.quit()


def on_closing(event=None):
    """ Lida com a ação de apertar o botão de fechar """
    client_socket.close()
    window.quit()


window = Tk()
window.title("ChitChat")
window.geometry("1280x720")
msg = StringVar()

# Message Frame (Frame -> Quadro que contem as mensagens)
messages_frame = Frame(window)
scrollbar = Scrollbar(messages_frame)
scrollbar.pack(side=TK_RIGHT, fill=TK_Y)

# Message List (ListBox -> Faz a exibição das mensagens dentro do frame)
messages_list = Listbox(messages_frame, width=200, height=35, yscrollcommand=scrollbar.set)
messages_list.pack(side=TK_LEFT, fill=TK_BOTH)
messages_list.pack()

messages_frame.pack()

# Message Box (Entry -> Campo de texto aberto para edição)
msg_box = Entry(window, textvariable=msg, width=200)
msg_box.bind("<Return>", send_message)
msg_box.pack()

send_button = Button(window, text="Send", command=send_message)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

BUFFER_SIZE = 1024
if __name__ == '__main__':
    try:
        HOST = input('Entre o IP do servidor: ')
        PORT = int(input('Entre a porta do servidor: '))
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        receive_thread = Thread(target=receive_message)
        receive_thread.start()
        tkinter.mainloop()
    except ConnectionError as cex:
        print("O servidor está indisponível no momento!")
