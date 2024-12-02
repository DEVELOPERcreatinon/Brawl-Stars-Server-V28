import socket
import time
import os
from threading import *
import sqlite3
from database.DataBase import DataBase
from Logic.Device import Device
from Logic.Player import Players
from Logic.LogicMessageFactory import packets
from Logic.LobbyInfoMessage import LobbyInfoMessage
from Utils.Helpers import Helpers
import json
import logging
import socket
import time
import os
from threading import *

from Logic.Device import Device
from Logic.Player import Players

from colorama import Fore;
from colorama import Style;
print(Fore.CYAN + f"[UPDATE]",Fore.MAGENTA + f"BRAWL SERVER",Fore.RED +"")
logging.basicConfig(filename="", level=logging.INFO, filemode="w")


def _(*args):
	print(Fore.RED + '[INFO]', end=' ')
	for arg in args:
		print(arg, end=' ')
	print()


class Server:
	Clients = {"ClientCounts": 0, "Clients": {}}
	ThreadCount = 0

	def __init__(self, ip: str, port: int):
		self.server = socket.socket()
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.port = port
		self.ip = ip

	def start(self):
		if not os.path.exists('./config.json'):
			print("Creating config.json...")
			Config.create_config(self)



		self.server.bind((self.ip, self.port))
		_(Fore.YELLOW + f'V28 BRAWL SERVER',Fore.GREEN +f'SERVER IP {self.ip} PORT SERVER {self.port}')
		while True:
			self.server.listen()
			client, address = self.server.accept()
			_(Fore.YELLOW + f'NEW PLAYER!',Fore.GREEN +f' IP {address[0]}')
			ClientThread(client, address).start()
			Server.ThreadCount += 1


class ClientThread(Thread):
	def __init__(self, client, address):
		super().__init__()
		self.client = client
		self.address = address
		self.device = Device(self.client)
		self.player = Players(self.device)

	def recvall(self, length: int):
		data = b''
		while len(data) < length:
			s = self.client.recv(length)
			if not s:
				print(Fore.RED +"ERROR!")
				break
			data += s
		return data

	def run(self):
		last_packet = time.time()
		try:
			while True:
				header = self.client.recv(7)
				if len(header) > 0:
					last_packet = time.time()
					packet_id = int.from_bytes(header[:2], 'big')
					length = int.from_bytes(header[2:5], 'big')
					data = self.recvall(length)

					if packet_id in packets:
						_(Fore.YELLOW + f'Received packet',Fore.MAGENTA + f'with ID {packet_id}.',Fore.GREEN + "")
						message = packets[packet_id](self.client, self.player, data)
						message.decode()
						message.process()

						if packet_id == 10101:
							Server.Clients["Clients"][str(self.player.low_id)] = {"SocketInfo": self.client}
							Server.Clients["ClientCounts"] = Server.ThreadCount
							self.player.ClientDict = Server.Clients

					else:
						_(Fore.YELLOW + f'Packet',Fore.MAGENTA +f'{packet_id} NOT HANDLED!')

				if time.time() - last_packet > 10:
					print(Fore.CYAN + f"[INFO]",Fore.GREEN + f"Ip: {self.address[0]}",Fore.RED + f"disconnected! (code bag)")
					self.client.close()
					break
		except ConnectionAbortedError:
			print(Fore.CYAN + f"[INFO]",Fore.GREEN + f"IP: {self.address[0]}",Fore.RED + f"DISCONNECTED! (Connection Aborted)")
			self.client.close()
		except ConnectionResetError:
			print(Fore.CYAN + f"[INFO]",Fore.GREEN + f"IP: {self.address[0]}",Fore.RED + f"DISCONNECTED! (Connection Reset)")
			self.client.close()
		except TimeoutError:
			print(Fore.CYAN + f"[INFO]",Fore.GREEN + f"IP: {self.address[0]}",Fore.RED + f"DISCONNECTED! (Time out)")
			self.client.close()


if __name__ == '__main__':
	server = Server('0.0.0.0', 25665)
	server.start()