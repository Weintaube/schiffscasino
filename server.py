import socket
from threading import Thread

host = '127.0.0.1'  # server name
port = 5000


class Server:

    def __init__(self):
        self.clients = []
        self.usernames = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO parameter
        self.socket.bind(('', port))  # bind the socket with server and port number
        self.socket.listen(3)  # allow maximum 3 connections to server
        print("Server is now listening...")

    def accept_connections(self):
        client, addr = self.socket.accept()  # accept new client
        print("New connection")
        client.send(str.encode("You are now connected to the server! If you want to close the connection type STOP!"))

        new_thread = Thread(target=self.on_new_client, args=[client])  # start thread for new client
        new_thread.start()

    def on_new_client(self, client):
        username = client.recv(1024).decode()  # username first msg
        print(username + " has registered")

        self.clients.append(client)  # append new user to lists
        self.usernames.append(username)

        client.send(str.encode("Hello " + username + "! Welcome to the chat room!"))
        while True:
            msg = client.recv(1024).decode()  # receive a msg
            if msg == "STOP":  # client is leaving chat
                print(username + " is leaving the chat")
                for c in self.clients:  # inform chat about leaving user
                    c.send(str.encode(username + " is leaving the chat"))

                index = self.usernames.index(username)  # remove client from list
                del (self.usernames[index])
                del (self.clients[index])
                break
            print(username + ": " + msg)
            for c in self.clients:  # send msg to every client
                c.send(str.encode(username + ": " + msg))


server = Server()
while True:
    server.accept_connections()
