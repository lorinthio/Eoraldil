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
		player.client = self
		self.player = player
		self.moved_players = {}
		self.removed_players = []
		self.spawnedMobs = []
		self.movedMobs = None
		self.send_loc = False
		connection.Send({"action": "nickname", "nickname": player.name})

	def sendLocation(self):
		player = self.player
		connection.Send({"action": "position", "position": (player.x, player.y)})
	
	def Loop(self):
		if self.send_loc:
			self.sendLocation()
			self.send_loc = False
		connection.Pump()
		self.Pump()
	
	def sendMessage(self, line):
		connection.Send({"action": "message", "message": line})
	
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
		self.message("[" + (data['who'].split())[0] + "] : " + data['message'], libtcod.light_green)
		#print(data['who'] + ": " + data['message'])

	def Network_systemMessage(self, data):
		self.message(data['message'], libtcod.yellow)

	def Network_systemSentMessage(self, data):
		self.message(data['message'], libtcod.light_purple)

	def message(self, message, color):
		self.gui.message(message, color)
	
	def Network_playerDisconnect(self, data):
		self.removed_players.append(data['who'])
		self.message(data['who'] + " has disconnected", libtcod.yellow)
	
	def Network_map(self, data):
		width = data['width']
		self.singlechunksize = float(100 * (1.0 / width))
		self.count = 0
		self.i = 0		
	
		self.mapData = data
		self.mapDone = False
		self.message("Loading " + data['mapType'] + " at location... " + str(data['location']), libtcod.yellow)
		
	def Network_mapChunk(self, data):
		self.count += self.singlechunksize
		if self.count >= 10:
		    self.count -= 10
		    self.i += 1
		    self.message("Loaded " + str(10 * self.i) + "%", libtcod.yellow)
		#self.gotChunk = True
		self.chunks.append(data['chunk'])
		
	def Network_mapDone(self, data):
		self.message("Initializing map", libtcod.yellow)
		self.mapDone = True
		self.mapChange = True

        def Network_mobSpawn(self, data):
                self.spawnedMobs.append(data)

        def Network_mobAction(self, data):
		keys = data['mobinfo'].keys()
		for key in keys:
			if data['mobinfo'][key][1] != None:
				mobname = data['mobinfo'][key][1][0]
				attack = data['mobinfo'][key][1][1]
				target = data['mobinfo'][key][1][2]
				damage = data['mobinfo'][key][1][3]
				if target == self.player.name:
					self.message(mobname + " used " + attack + " on you for " + str(damage) + " damage", libtcod.red)
					self.player.curClass.hp -= damage
				else:
					self.message(mobname + " used " + attack + " on " + target +  " for " + str(damage) + " damage", libtcod.orange)
                self.movedMobs = data
		
	def Network_position(self, data):
		if data['who'] != self.player.name:
			print data['who'], data['position']
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
