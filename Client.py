import sys
from time import sleep
from sys import stdin, exit
from GUI import *

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *
from sys import *

class Client(ConnectionListener):
	def __init__(self, host, port, player, gui):
		self.mapChange = False
		self.Connect((host, port))
		print "Client started"
		self.chunks = []
		self.gui = gui
		self.player = player
		self.moved_players = {}
		self.removed_players = []
		self.spawnedMobs = []
		self.movedMobs = None
		self.send_loc = False
		connection.Send({"action": "nickname", "nickname": player.name})
		t = start_new_thread(self.InputLoop, ())
		
	def sendLocation(self):
		player = self.player
		connection.Send({"action": "position", "position": (player.x, player.y)})
	
	def Loop(self):
		if self.send_loc:
			self.sendLocation()
			self.send_loc = False
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
		self.message(data['who'] + ": " + data['message'], libtcod.light_green)
		#print(data['who'] + ": " + data['message'])

	def message(self, message, color):
		self.gui.message(message, color)
	
	def Network_playerDisconnect(self, data):
		self.removed_players.append(data['who'])
		self.message(data['who'] + " has disconnected", libtcod.yellow)
	
	def Network_map(self, data):
		self.mapChange = True
		self.mapData = data
		self.mapDone = False
		
	def Network_mapChunk(self, data):
		self.gotChunk = True
		self.chunks.append(data['chunk'])
		
	def Network_mapDone(self, data):
		self.mapDone = True

        def Network_mobSpawn(self, data):
                self.spawnedMobs.append(data)

        def Network_mobsMove(self, data):
                self.movedMobs = data
		
	def Network_position(self, data):
		self.moved_players[data['who']] = data['position']
	
	# built in stuff

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print ("network error")
		print data['error']
		connection.Close()
	
	def Network_disconnected(self, data):
		print data
		exit()
