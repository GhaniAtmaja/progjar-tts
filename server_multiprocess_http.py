from socket import *
import socket
import multiprocessing
import time
import sys
import logging
from http import HttpServer

httpserver = HttpServer()

def ProcessClient(connection, address):
	rcv=""
	while True:
		try:
			data = connection.recv(32)
			if data:
				#merubah input dari socket (berupa bytes) ke dalam string
				#agar bisa mendeteksi \r\n
				d = data.decode()
				rcv=rcv+d
				if rcv[-2:]=='\r\n':
					#end of command, proses string
					# logging.warning("data dari client: {}" . format(rcv))
					hasil = httpserver.proses(rcv)
					#hasil akan berupa bytes
					#untuk bisa ditambahi dengan string, maka string harus di encode
					hasil=hasil+"\r\n\r\n".encode()
					# logging.warning("balas ke  client: {}" . format(hasil))
					#hasil sudah dalam bentuk bytes
					connection.sendall(hasil)
					rcv=""
					connection.close()
			else:
				break
		except OSError as e:
			pass
	connection.close()


class Server(object):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0', 8889))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			# logging.warning("connection from {}".format(self.client_address))


			multiprocessing.Process(target=ProcessClient, args=(self.connection, self.client_address)).start()
			# ProcessClient(self.connection, self.client_address)



def main():
	svr = Server()
	svr.run()

if __name__=="__main__":
	main()

