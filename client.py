import socket
from socket import socket
from threading import Thread


host = '127.0.0.1'  # server name
port = 5000  # port name

class Client:
	def __init__(self):  # instance variables
		self.stop = False
		self.client_socket = socket()  # instantiate
		print("Waiting for connection")
		self.client_socket.connect((host, port))  # connect to the server

	def send(self, message):
		self.client_socket.send(message.encode())
		return self.client_socket.recv(1024).decode()

'''import socket
import sys
from threading import Thread
from socket import socket

host = '127.0.0.1'  # server name
port = 5000  # port name


class Client:
	def __init__(self):  # instance variables
		self.stop = False
		self.client_socket = socket()  # instantiate
		self.client_socket.connect((host, port))  # connect to the server
		print("Waiting for connection")

	def receive(self):
		username = input("Username: ")
		self.client_socket.send(username.encode()) #first, send username to server

		while True:
			try:
				if self.stop: #exiting thread
					sys.exit()

				message = self.client_socket.recv(1024).decode() #receive msg from server
				print(message)
			except:
				self.client_socket.close()
				break

	def write(self):
		while True: #take input from console
			message = input()
			self.client_socket.send(message.encode()) #send to server
			if message == "STOP":
				self.stop = True
				sys.exit()


client = Client()

recv_thread = Thread(target=client.receive) #thread for receiving msgs
recv_thread.start()

write_thread = Thread(target=client.write) #thread for writing msgs
write_thread.start()'''
