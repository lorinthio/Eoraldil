import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *
from sys import *

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.mapChange = False
		self.Connect((host, port))
		print "Client started"
		self.chunks = []
	
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	def InputLoop(self):
		# horrid threaded input loop
		# continually reads from stdin and sends whatever is typed to the server
		while 1:
			connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
	
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	def Network_players(self, data):
		print "*** players: " + ", ".join([p for p in data['players']])
	
	def Network_message(self, data):
		print data['who'] + ": " + data['message']
	
	def Network_map(self, data):
		self.mapChange = True
		self.mapData = data
		self.mapDone = False
		
	def Network_mapChunk(self, data):
		self.gotChunk = True
		self.chunks.append(data['chunk'])
		
	def Network_mapDone(self, data):
		self.mapDone = True
	
	# built in stuff

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print ("network error")
		print data['error']
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

def main():
	host = "localhost"
	port = "12345"
	c = Client(host, int(port))
	while 1:
		c.Loop()
		sleep(0.001)
