import socket
import threading
import sys
import sqlite3

bData = ""
class Server:
	def deleteUsers(self):
		conn = sqlite3.connect('backup.db')
		print("Opened database successfully");
		c = conn.cursor()
		sql = "DELETE FROM users"
		c.execute(sql)
		conn.commit()
		
	def deleteTodos(self):
		conn = sqlite3.connect('backup.db')
		print("Opened database successfully");
		c = conn.cursor()
		sql = "DELETE FROM todo"
		c.execute(sql)
		conn.commit()
		
	def insertIntoDb(self, data):
		result = data.split("::")
		if result[0] == "..1..":
			self.deleteUsers()
		if result[0] == "..2..":
			self.deleteTodos()
		conn = sqlite3.connect('backup.db')
		print("Opened database successfully");
		c = conn.cursor()
		if result[0] == "..1..":
			for r in result:
				x = r.split(";")
				try:
					print("a")
					sql = "INSERT INTO users(username, password) VALUES ('%s', '%s')" %(x[2], x[3])
					c.execute(sql)
					print("b")
					conn.commit()
				except:
					print("c")
					conn.rollback()
		if result[0] == "..2..":
			for r in result:
				x = r.split(";")
				try:
					print("a")
					sql = "INSERT INTO todo(username, todos) VALUES ('%s', '%s')" %(x[2], x[3])
					c.execute(sql)
					print("b")
					conn.commit()
				except:
					print("c")
					conn.rollback()


	def __init__(self, ServerIp, ServerPort):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((ServerIp, ServerPort))
		sock.listen(1)
		
		while True:
			c, a = sock.accept()
			cThread = threading.Thread(target=self.handler, args=(c, a))
			cThread.daemon = True
			cThread.start()
			print(str(a[0]) + ':' + str(a[1]), "connected")
	def handler(self, c, a):
		global bData
		while True:
			data = c.recv(1024)
			if data:
				print(str(a[0]) + ':' + str(a[1]) + ":- " + str(data, 'utf-8'))
				bData = str(data, 'utf-8')
				self.insertIntoDb(bData)
				
			if not data:
				#print(str(a[0]) + ':' + str(a[1]) + str(data, 'utf-8'), "disconnected")
				#self.connections.remove(c)
				c.close()
				break

class Client:
	def sendMsg(self, sock):
		while True:
			sock.send(bytes(input(""), 'utf-8'))
	def __init__(self, address, ServerPort):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((address, ServerPort))
		iThread = threading.Thread(target=self.sendMsg, args=(sock,))
		iThread.daemon = True
		iThread.start()
		
		while True:
			data = sock.recv(1024)
			if not data:
				break
			print(str(data, 'utf-8'))



server = Server("192.168.0.100", 10050)















		

