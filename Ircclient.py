import sys
import socket
import select
import errno
import time


class Ircclient:



	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.IP = "127.0.0.1"
		self.port = 1234
		self.length = 1024


	def connection(self):
		self.username = input('please enter your nickname: ')
		print('To join channel enter "/join" followed by channel name, to leave channel type "/leave" followed by channel name, to list clients type "/list", to list client in a channel type "/usrnchan" followed by channel name, to list channels type "listchannels", to send message to a channel type "/sendmsgto" followed bt channel name followed by message, and to leave the entire server type "/quit"')
		self.socket.connect((self.IP, self.port))

		self.socket.setblocking(False)
		username = self.username.encode('utf-8')
		username_header = f"{len(username):<{self.length}}".encode('utf-8')
		self.socket.send(username_header + username)
		sys.stdout.write('your message: ')
		sys.stdout.flush()


		while True:
			read, write, x = select.select([0, self.socket], [], [])
			if not read:
				continue
			for r in read:
				if r == 0:
					message = input()
					
					if message == '/list':
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('user list: {}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue

						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()

					elif message.startswith('/join'):
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('{}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue

						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()

					elif message.startswith('/leave'):
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('{}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue
						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()

					elif message.startswith('/usrnchan'):
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('users in this channel are: {}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue
						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()

					elif message.startswith('/listchannels'):
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('channels are: {}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue
						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()

					elif message.startswith('/quit'):
						message = message.encode('utf-8')
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('{}'.format(message))
								self.socket.close()
								sys.exit()
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								sys.exit()
							continue
						except Exception as e:
							print('Error {}'.format(e))
							sys.exit()


					elif message.startswith('/sendmsgto'):
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						message = message.encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('{}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								
							continue
						except Exception as e:
							print('Error {}'.format(e))
							
					elif message.startswith('/privmsg'):
						message_header = f"{len(message) :< {self.length}}".encode('utf-8')
						message = message.encode('utf-8')
						self.socket.send(message_header + message)
						try:
							while True:
								time.sleep(0.2)
								message_header = self.socket.recv(1024)
								message_length = int(message_header.decode('utf-8').strip())
								message = self.socket.recv(message_length).decode('utf-8')
								print('{}'.format(message))
								break

						except IOError as e:
							if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
								print('Reading error: {}'.format(str(e)))
								
							continue
						except Exception as e:
							print('Error {}'.format(e))
							



					else:
						print('command not found! please provide command from descriptions')

					sys.stdout.write('your message: ')
					sys.stdout.flush()

				elif r == self.socket:
					username_header = self.socket.recv(1024)
					if not len(username_header):
						print("connection closed by server")
						sys.exit()

					username_length = int(username_header.decode('utf-8').strip())
					username = self.socket.recv(username_length).decode('utf-8')

					chnl_header = self.socket.recv(1024)
					chnl_length = int(chnl_header.decode('utf-8').strip())
					chnl = self.socket.recv(chnl_length).decode('utf-8')

					message_header = self.socket.recv(1024)
					message_length = int(message_header.decode('utf-8').strip())
					message = self.socket.recv(message_length).decode('utf-8')

					print('{} {}: {}'.format(username, chnl, message))

					#sys.stdout.write('your message: ')
					#sys.stdout.flush()
				


			

if __name__ == '__main__':
    client = Ircclient()
    client.connection()