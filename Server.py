import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from sys import *
sys.path.append('.//PodSixNet')
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from MapObject import *
from threading import *
from Monster import *
import time
import select

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
        for playerObj in self._server.playerObjects:
            if playerObj.address == self:
                playerObj.name = self.nickname
                break
        
        
    def Network_position(self, data):
        data = {"action": "position", "position": data['position'], "who": self.nickname}
        self.position = data['position']
        for playerObj in self._server.playerObjects:
            if playerObj.address == self:
                playerObj.position = self.position
                break        
        self._server.SendToAllButPlayer(data, self)
        

class EoraldilServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        self.playerObjects = []
        #Puts all connections in this map
        self.players = WeakKeyDictionary()
        
        #Makes the regions from scratch
        self.MH = MonsterHandler()
        self.generateWorld(4)
            
        Server.__init__(self, *args, **kwargs)
        print 'Server launched'
        #t = start_new_thread(self.InputLoop, ())
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        #mess = stdin.readline()
        #print mess
        #if mess == "newmap":
        #    self.genMap()
        #    for player in self.players:
        #        self.sendMap(player)
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line:
                print line
            else: # an empty line means stdin has been closed
                print('eof')
                exit(0)

    def sendMap(self, player):
        region = self.regions[0]
        Map = region.Map
        data = {"action": "map",  
                    "startingPoint": Map.starting_point,
                    "width": Map.width,
                    "height": Map.height,
                    "fovRange": Map.fov_range,
                    "mapType": Map.mapType}
        player.Send(data)
        for x in range(Map.width):
            mappedarea = {}
            for y in range(Map.height):
                tile = Map.mappedArea[x][y]
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
        print("sending mobs")
    
    def AddPlayer(self, player):
        self.sendMap(player)
        self.sendMobs(player)  
        print "sending map"
        self.SendPlayersInMap(player)
        self.players[player] = True
        newplayer = EntityObject(1, 1)
        newplayer.address = player
        newplayer.name = ""
        self.playerObjects.append(newplayer)
    
    def DelPlayer(self, player):
        for p in self.players:
            data = {"action": "playerDisconnect", "who": player.nickname}
            p.Send(data)

    def sendMobs(self, player):
        region = self.regions[0]
        for mob in region.mobs:
            data = {"action": "mobSpawn",
                        "name": mob.name,
                        "id": mob.ID,
                        "position": (mob.x, mob.y),
                        "char": mob.char,
                        "color": (mob.color.r, mob.color.g, mob.color.b)}
            player.Send(data)
            time.sleep(0.1)
            #if isinstance(mob, Creature):
            #elif isinstance(mob, Monster):
                

    def SendPlayersInMap(self, player):
        for p in self.players:
            data = {"action": "position", "position": p.position, "who": p.nickname}
            player.Send(data)
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def SendToAllButPlayer(self, data, player):
        for p in self.players:
            if p is not player:
                p.Send(data)
    
    def generateWorld(self, regions):
        print "Generating World..."
        self.regions = []
        for i in range(regions):
            region = Region(self.MH)
            self.regions.append(region)
        print "Generated World with", regions, "regions"
    
    def serverLoop(self):
        sleep(0.001)
    
    def automateMobs(self, deltaT):
        region = self.regions[0]
        mobdata = {}
        for mob in region.mobs:
            action = mob.takeAction(deltaT, region.Map, region.objects)
            if action:
                mobdata[mob.ID] = (mob.x, mob.y)
            
        data = {"action": "mobsMove", "mobinfo": mobdata}
                
    def Launch(self):
        timer = Timer()
        frame = 0
        while True:
            self.automateMobs(frame)
            self.Pump()
            self.serverLoop()
            frame = timer.nextFrame()
            
class Timer:
    
    def __init__(self):
        self.curTime = time.time()
        
    def nextFrame(self):
        frame = time.time() - self.curTime
        self.curTime = time.time()
        
        return frame

def main():
    host = "localhost"
    port = "25565"
    s = EoraldilServer(localaddr=(host, int(port)))
    s.Launch()
    
main()


