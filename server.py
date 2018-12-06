#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio1.py
# Asynchronous I/O inside "asyncio" callback methods.

import asyncio, zen_utils
import db

chat = {'all':{'message':[]}}

class Server(asyncio.Protocol):

	def connection_made(self, transport):
		self.transport = transport
		self.address = transport.get_extra_info('peername')
		self.data = b''
		self.item = self.address[0]+":"+str(self.address[1])
		chat[self.item] = {'name': '', 'message':[]}
		print('Accepted connection from {}'.format(self.address))

	def data_received(self, data):
		self.data += data
		# print(chat[self.item]['name'])
		if chat[self.item]['name'] == '':
			if b'login' in self.data:
				x = str(self.data).split(' ')
				# print(x)
				if len(x) == 3 and 'login' in x[0]:    # 处理登录
					username = x[1]
					password = x[2]
					if(db.login(username,password)):
						chat[self.item]['name'] = username
						print(chat[self.item]['name']+' login')
						self.transport.write(b'login seccessful')
					else:
						self.transport.write(b'username or password not right')

			if b'register' in self.data:    # 处理用户注册
				x = str(self.data).split(' ')
				# print(x)
				if len(x) == 3 and  'register' in x[0]:

					username = x[1]
					password = x[2]
					if(db.register(username,password)):
						chat[self.item]['name'] = username
						self.transport.write(b'register seccessful')
					else:
						self.transport.write(b'register bad')
				else:
					print('register bad')

		if chat[self.item]['name'] == '' :
			self.transport.write(b'please login  ')
		else:
			if self.data.endswith(b'$'):
				if b':' in self.data:        # 判断是否私聊
					siliao = self.data.decode()
					people = siliao.split(':')
					# print(people[0])
					# print(chat)
					for i in chat.keys():
						try:
							if chat[i]['name'] == str(people[0]):
								message = "{}-->".format(chat[self.item]['name'])+people[1] 
								chat[i]['message'].append(message.encode())
						except:
							pass
				else:
					answer = self.data
					# chat[self.item]['message'].append(chat[self.item]['name'].encode()+b' : '+answer)
					# print(chat)
					chat['all']['message'].append(chat[self.item]['name'].encode()+b' : '+answer)
			else:
				for i in chat['all']['message']:
					self.transport.write(i)
				for i in chat[self.item]['message']:
					self.transport.write(i)
					print(i+b'\n')
		# print(self.data)

		self.data = b''

	def connection_lost(self, exc):
		if exc:
			print('Client {} error: {}'.format(self.address, exc))
		elif self.data:
			print('Client {} sent {} but then closed'.format(self.address, self.data))
		else:
			print('Client {} closed socket'.format(self.address))

if __name__ == '__main__':
	address = ('127.0.0.1', '8889')
	loop = asyncio.get_event_loop()
	coro = loop.create_server(Server, *address)
	server = loop.run_until_complete(coro)
	print('Listening at {}'.format(address))
	try:
		loop.run_forever()
	finally:
		server.close()
		loop.close()
