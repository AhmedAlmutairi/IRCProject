import socket
import sys
import select
from Ircclient import *
import pickle



class Ircserver:


	def __init__(self):
		#create socket
		self.socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.host = "127.0.0.1"
		#server port
		self.port = 1234
		#store all sockets including server sockets
		self.sockets = []
		#dic that store the client sockets as keys and client information as values
		self.client_info = {}
		#message from clients
		self.header = ''
		self.messsage_length = 1024
		self.channels = {}
		self.chan_users = []

	#recieve messages from clients
	def messages(self, c_sockets):
		try:
			header = c_sockets.recv(1024)
			messsage_length = int(header.decode('utf-8').strip())
			return {'header': header, 'data': c_sockets.recv(messsage_length)}
		except Exception as e:
			return False

	def cmd_message(self, cmd, chan_name, s):
		client = self.client_info[s]
		user = client['data'].decode('utf-8')
		if cmd == '/join':
			chnl = chan_name.decode('utf-8')
			if not chnl.startswith('#'):
					chnl = '#' + chnl
			if chnl not in self.channels:
				self.channels[chnl] = []
			if user not in self.channels[chnl]:
				chan_clients = {chan_name: [user]}
				self.channels[chnl].append(user)
				for key in self.channels.keys():
					print("keys are : {}".format(key)) 
				for c in self.channels.keys():
					print('channel users: {}'.format(self.channels))
				response = 'you joined channel ' + chnl
				response = response.encode('utf-8')
				message_header = f"{len(response) :< {1024}}".encode('utf-8')
				s.send(message_header + response)
			else:
				response = 'you are already joined ' + chnl
				response = response.encode('utf-8')
				message_header = f"{len(response) :< {1024}}".encode('utf-8')
				s.send(message_header + response)
		elif cmd == '/list':
			users = []
			for clt in self.client_info.values():
				users.append(clt['data'].decode('utf-8'))
			user_list = ', '
			user_list = user_list.join(users)
			user_list = user_list.encode('utf-8')
			message_header = f"{len(user_list) :< {1024}}".encode('utf-8')
			s.send(message_header + user_list)
		elif cmd == '/usrnchan':
			users = []
			chnl = chan_name.decode('utf-8')
			if not chnl.startswith('#'):
					chnl = '#' + chnl
			if chnl not in self.channels.keys():
				response = chnl + ' is not found'
				response = response.encode('utf-8')
				message_header = f"{len(response) :< {1024}}".encode('utf-8')
				s.send(message_header + response)
			else:
				for u in self.channels[chnl]:
					users.append(u)
				user_list = ', '
				user_list = user_list.join(users)
				user_list = user_list.encode('utf-8')
				message_header = f"{len(user_list) :< {1024}}".encode('utf-8')
				s.send(message_header + user_list)
		elif cmd == '/listchannels':
			channels = []
			for u in self.channels.keys():
				channels.append(u)
			chnl_list = ', '
			chnl_list = chnl_list.join(channels)
			chnl_list = chnl_list.encode('utf-8')
			message_header = f"{len(chnl_list) :< {1024}}".encode('utf-8')
			s.send(message_header + chnl_list)
		elif cmd == '/leave':
			chnl = chan_name.decode('utf-8')
			if not chnl.startswith('#'):
				chnl = '#' + chnl
			if user in self.channels[chnl]:
				self.channels[chnl].remove(user)
				response = 'you left channel ' + chnl
				response = response.encode('utf-8')
				message_header = f"{len(response) :< {1024}}".encode('utf-8')
				s.send(message_header + response)
			else:
				response = 'you are not in channel ' + chnl
				response = response.encode('utf-8')
				message_header = f"{len(response) :< {1024}}".encode('utf-8')
				s.send(message_header + response)
		elif cmd == '/privmsg':
			client = self.client_info[s]
			user = chan_name[0]
			str_msg = []
			user = user.decode('utf-8')
			msg = chan_name[1:]
			for i in msg:
				str_msg.append(i.decode('utf-8'))
			message = ' '
			message = message.join(str_msg)
			message_header = f"{len(message) :< {1024}}".encode('utf-8')
			message = message.encode('utf-8')
			response = 'A private message from'
			response_header = f"{len(response) :< {1024}}".encode('utf-8')
			response = response.encode('utf-8')
			for clt in self.client_info:
				username = self.client_info[clt]
				username = username['data']
				if username.decode('utf-8') == user:
							clt.send(response_header + response + client['header'] + client['data'] + message_header + message)

	#send message to clients with a channel	
	def send_message_to(self, chnl, msg, s):
		client = self.client_info[s]
		str_msg = []
		chnl = chnl.decode('utf-8')
		if not chnl.startswith('#'):
			chnl = '#' + chnl
		if chnl not in self.channels.keys():
			response = chnl + ' is not found'
			response = response.encode('utf-8')
			message_header = f"{len(response) :< {1024}}".encode('utf-8')
			s.send(message_header + response)
		elif client['data'].decode('utf-8') not in self.channels[chnl]:
			response = 'you have to join ' + chnl + ' before sending message to it'
			response = response.encode('utf-8')
			message_header = f"{len(response) :< {1024}}".encode('utf-8')
			s.send(message_header + response)
		else:
			for i in msg:
				str_msg.append(i.decode('utf-8'))
			message = ' '
			message = message.join(str_msg)
			message_header = f"{len(message) :< {1024}}".encode('utf-8')
			message = message.encode('utf-8')

			from_chnl = 'from channel: ' + chnl
			from_chnl = from_chnl.encode('utf-8')
			chnl_header = f"{len(from_chnl) :< {1024}}".encode('utf-8')
			for clt in self.client_info:
				username = self.client_info[clt]
				username = username['data']
				if clt != s:
					for u_n_c in self.channels[chnl]:
						if username.decode('utf-8') == u_n_c:
							clt.send(client['header'] + client['data'] + chnl_header + from_chnl + message_header + message)



	def read_write_sockets(self):
		self.socket.bind((self.host, self.port))
		self.socket.listen()
		self.sockets = [self.socket]
		print("server is listening on {}, {}".format(self.host, self.port))

		while True:
			read_sockets, write_sockets, exception_sockets = select.select(self.sockets, [], self.sockets)
			for s in read_sockets:
				if s == self.socket:
					connection, address = self.socket.accept()
					connection.setblocking(False)
					user_data = self.messages(connection)
					if user_data is False:
						print("user is false")
						self.sockets.remove(s)
						#delete client information
						del self.client_info[s]
						continue

					else:
						#add new client's socket to the list of sockets
						self.sockets.append(connection)

						#add user information to client list
						self.client_info[connection] = user_data
						print("user data ".format(user_data['data'].decode('utf-8')))
						print('new client is connected on {}, {}, nickname: {}'.format(address[0], address[1], user_data['data'].decode('utf-8')))

				else:
					#recieve message from existed client and send it to message function
					client_messages = self.messages(s)
					#print("client messages {}".format(client_messages))
					if client_messages is False:
						username = self.client_info[s]
						username = username['data'].decode('utf-8')
						print('close connection from {}'.format(self.client_info[s]['data'].decode('utf-8')))
						for chan in self.channels.keys():
							for usr in self.channels[chan]:
								if usr == username:
									self.channels[chan].remove(usr)
									print('channel users: {}'.format(self.channels))
						#remove client from socket list
						self.sockets.remove(s)
						#delete client information
						del self.client_info[s]
						continue
					user_data = self.client_info[s]
					slt = client_messages['data'].split()
					cmd = slt[0].decode('utf-8')

					_ = ''
					if cmd == '/join':
						if len(slt) < 2:
							response = 'please provide channel name you want to join'
							response = response.encode('utf-8')
							message_header = f"{len(response) :< {1024}}".encode('utf-8')
							s.send(message_header + response)
						else:
							self.cmd_message(cmd, slt[1], s)
					elif cmd == '/leave':
						if len(slt) < 2:
							response = 'please provide channel name you want to leave'
							response = response.encode('utf-8')
							message_header = f"{len(response) :< {1024}}".encode('utf-8')
							s.send(message_header + response)
						else:
							self.cmd_message(cmd, slt[1], s)
					elif cmd == '/list':
						self.cmd_message(cmd, _, s)

					elif cmd == '/usrnchan':
						if len(slt) < 2:
							response = 'please provide channel name you want to list its users'
							response = response.encode('utf-8')
							message_header = f"{len(response) :< {1024}}".encode('utf-8')
							s.send(message_header + response)
						else:
							self.cmd_message(cmd, slt[1], s)
					elif cmd == '/listchannels':
						self.cmd_message(cmd, _, s)
					elif cmd == '/sendmsgto':
						if len(slt) < 2:
							response = 'please provide channel name you want to send your message to'
							response = response.encode('utf-8')
							message_header = f"{len(response) :< {1024}}".encode('utf-8')
							s.send(message_header + response)
						else:
							self.send_message_to(slt[1], slt[2:], s)
					elif cmd == '/privmsg':
						if len(slt) < 2:
							response = 'please provide user nickname'
							response = response.encode('utf-8')
							message_header = f"{len(response) :< {1024}}".encode('utf-8')
							s.send(message_header + response)
						else:
							self.cmd_message(cmd, slt[1:], s)
					elif cmd == '/quit':
						username = self.client_info[s]
						username = username['data'].decode('utf-8')
						print(username)
						for chan in self.channels.keys():
							for usr in self.channels[chan]:
								if usr == username:
									self.channels[chan].remove(usr)
									print('channel users: {}'.format(self.channels))
						response = 'Goodbye ' + user_data['data'].decode('utf-8')
						response = response.encode('utf-8')
						message_header = f"{len(response) :< {1024}}".encode('utf-8')
						s.send(message_header + response)
						self.sockets.remove(s)
						del self.client_info[s]
						s.close()

			#remove all error sockets
			for s in exception_sockets:
				self.sockets.remove(s)
				del self.client_info[s]
	
if __name__ == '__main__':
    server = Ircserver()
    server.read_write_sockets()

