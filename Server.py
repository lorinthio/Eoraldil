import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from sys import path as syspath
syspath.append('.//PodSixNet')
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from MapObject import *
import time

class ClientChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		self.nickname = "anonymous"
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_message(self, data):
		self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
	
	def Network_nickname(self, data):
		self.nickname = data['nickname']
		self._server.SendPlayers()
		
	def Network_position(self, data):
		data = {"action": "position", "position": data['position'], "who": self.nickname}
		self._server.SendToAllButPlayer(data, self)
		

class ChatServer(Server):
	channelClass = ClientChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		self.genMap()
		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def AddPlayer(self, player):
		data = {"action": "map",  
	                "startingPoint": self.Map.starting_point,
	                "width": self.Map.width,
	                "height": self.Map.height,
	                "fovRange": self.Map.fov_range,
	                "mapType": self.Map.mapType}
		player.Send(data)
		for x in range(self.Map.width):
			mappedarea = {}
			for y in range(self.Map.height):
				tile = self.Map.mappedArea[x][y]
				color = tile.color
				info = [tile.blocked, tile.block_sight, tile.tileType, (color.r, color.g, color.b)]
				mappedarea[str(y)] = info
			chunk = {"action": "mapChunk",
			        "chunk": mappedarea}
			player.Send(chunk)
			self.Pump()
			time.sleep(0.1)
		finished = {"action": "mapDone"}
		player.Send(finished)
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		print "players", [p for p in self.players]
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def SendToAllButPlayer(self, data, player):
		for p in self.players:
			if p is not player:
				p.Send(data)
	
	def genMap(self):
		self.Map = Map(None)
		print self.Map.width, self.Map.height
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.001)

def main():
	host = "localhost"
	port = "12345"
	s = ChatServer(localaddr=(host, int(port)))
	s.Launch()
	
main()


