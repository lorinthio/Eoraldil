import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from sys import *
sys.path.append('.//PodSixNet')
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from MapObject import *
from thread import *
from Monster import *
from Character import *
import time
import select
import traceback

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
        if data['message'][0] == "/":
            self.handle_command(data['message'])
        else:
            self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
            print "[" + self.nickname + "] : " + data['message']
    
    def handle_command(self, line):
        line = line.strip()
        if line == "/help":
            commands = ["/time", "/tp"]
            message = "Server Commands:\n"
            self.Send({"action": "systemMessage", "message": message})
            for command in commands:
                message = command
                self.Send({"action": "systemMessage", "message": message})
            
        if line == "/time":
            message = "Monday"
            self.Send({"action": "systemMessage", "message": message})
            
        if "/tp" in line:
            line = line.split()
            try:
                xCoord = int(line[1])
                yCoord = int(line[2])
            except:
                message = "Not enough arguments. Usage :: /tp x y"
                self.Send({"action": "systemMessage", "message": message})
                return
                
            loc = (xCoord, yCoord)
            
            regionexists = self._server.checkRegion(loc)
            if not regionexists:
                message = "Generating location at... " + str(loc)
                self.Send({"action": "systemMessage", "message": message})
            self._server.ChangePlayerRegion(self, loc)
    
    def Network_nickname(self, data):
        self.nickname = data['nickname']
        print self.nickname, "has connected."
        self.object.name = self.nickname
        #for playerObj in self._server.playerObjects:
            #if playerObj.address == self:
                #playerObj.name = self.nickname
                #playerObj.char = self.nickname[0]
                #break
        
    def Network_position(self, data):
        data = {"action": "position", "position": data['position'], "who": self.nickname}
        self.position = data['position']
        self.object.x = self.position[0]
        self.object.y = self.position[1]
        self._server.SendToAllButPlayer(data, self)
        

class EoraldilServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        #self.playerObjects = []
        #Puts all connections in this map
        self.players = WeakKeyDictionary()
        self.regions = {}
        
        #Makes the regions from scratch
        self.MH = MonsterHandler()
        self.generateWorld()
            
        Server.__init__(self, *args, **kwargs)
        print 'Server launched'
        printCastle()
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
        region = player.region
        print "Player loading into " + str(region.location)
        Map = region.Map
        data = {"action": "map",  
                    "startingPoint": Map.starting_point,
                    "location": region.location,
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
    
    def AddPlayer(self, player):
        self.players[player] = True
        newplayer = Player("Player")
        newplayer.address = player
        #self.playerObjects.append(newplayer)
        
        player.object = newplayer
        
        #start_new_thread(self.ChangePlayerRegion, (player, (0,0),))
        self.ChangePlayerRegion(player, (0, 0))
        
    def ChangePlayerRegion(self, player, location):
        regionexists = self.checkRegion(location)
        if not regionexists:
            self.makeRegion(location)
        init_region = self.regions[location]
        init_region.addPlayer(player, self)
        player.region = init_region
        
        #start_new_thread(self.sendMap, (player,))
        #start_new_thread(self.sendMobs, (player,))
        #start_new_thread(self.SendPlayersInMap, (player,))
        self.sendMap(player)
        self.sendMobs(player)  
        self.SendPlayersInMap(player)
    
    def DelPlayer(self, player):
        try:
            region = player.region
            region.removePlayer(player)
            for p in self.players:
                data = {"action": "playerDisconnect", "who": player.nickname}
                print player.nickname, "has disconnected"
                p.Send(data)
            del self.players[player]
        except:
            print "Problem in DelPlayer"
            traceback.print_exc()

    def sendMobs(self, player):
        region = player.region
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
    
    def generateWorld(self):
        print "Generating World..."
        #Make the 5 initial regions...
        self.makeRegion((0,0))
        #self.makeRegion((0,1))
        #self.makeRegion((1,0))
        #self.makeRegion((0,-1))
        #self.makeRegion((-1,0))
        
        #Regions ordered like...
        
        #      (0, 1)
        #(-1,0)(0, 0) (1, 0)
        #      (0,-1)
        
        #Could later add in weather patterns to move across the regions =D
        print "Finished generating world"
        
    def makeRegion(self, location):
        region = Region(self.MH, location=location)
        self.regions[location] = region
        
    def checkRegion(self, location):
        if location in self.regions:
            return True
        else:
            return False
            
        
    def serverLoop(self, frame):
        self.Pump()
        try:
            self.automateMobs(frame)
        except:
            pass        
        sleep(0.001)
    
    def automateMobs(self, deltaT):
        for loc in self.regions:
            #A region is active if a player is in it.
            region = self.regions[loc]
            if region.active:
                mobdata = {}
                for mob in region.mobs:
                    action = mob.takeAction(deltaT, region.Map, region.objects)
                    if action:
                        #data = (MoveData, AttackData)
                        #MoveData = (posx, posy)
                        #AttackData = (NameAttack, Damage, Target)
                        pos = None
                        attack = None
                        if mob.attacked != None:
                            attack = mob.attacked
                            mob.attacked = None
                        if mob.moved:
                            pos = (mob.x, mob.y)
                            mob.moved = False
                            
                        if pos != None or attack != None:
                            mobdata[mob.ID] = (pos, attack)
                    
                if mobdata != {}:
                    data = {"action": "mobAction", "mobinfo": mobdata}
                    for p in region.players:
                        p.address.Send(data)
                
    def Launch(self):
        timer = Timer()
        frame = 0
        listTest = [""]
        start_new_thread(inputLoop, (listTest, timer, self,))
        while listTest[0] != "stop":
            self.serverLoop(frame)
            frame = timer.nextFrame()
            #Time per tick
            #print frame
        self.stopServer()
        
    def stopServer(self):
        print "=================="
        print "Stopping Server..."
        print "=================="
        sleep(1)

def inputLoop(listTest, timer, server):
    user_in = raw_input()
    listTest[0] = user_in
    while(user_in != "stop"):
        #Commands!
        command = user_in.split()[0]
        
        if command == "time":
            timer.printFps()
        elif command == "say":
            message = "[Server]: " + user_in[4:]
            server.SendToAll({"action": "systemSentMessage", "message": message})
        
        user_in = raw_input()
        listTest[0] = user_in

class Timer:
    
    def __init__(self):
        self.curTime = time.time()
        self.fps = 0
        
    def nextFrame(self):
        frame = time.time() - self.curTime
        self.curTime = time.time()
        try:
            self.fps = 1.0 / frame
        except:
            pass
        
        return frame
    
    
    def printFps(self):
        print int(self.fps)

def main():
    host = "localhost" # Don't use localhost when broadcasting publically
    port = "25565"
    print "-------------------------------------"
    print 'Server launching at ' + host + ":" + port
    print "-------------------------------------"
    s = EoraldilServer(localaddr=(host, int(port)))
    s.Launch()
    
def printCastle():
    print "         ____                                         ____"
    print "         IIII                                         IIII"
    print "         ####                                         ####"
    print "         HHHH     Madness comes, and madness goes     HHHH"
    print "         HHHH    An insane place, with insane moves   HHHH"
    print "         ####   Battles without, for battles within   ####"
    print "      ___IIII___        Where evil lives,          ___IIII___"
    print "   .-'_._{**}_._`-.      and evil rules         .-'_._{**}_._`-."
    print "   |/`  .'\/`.  `\|    Breaking them up,        |/`  .'\/`.  `\|"
    print "   `    }    {    '   just breaking them in     `    }    {    '"
    print "        ) () (  Quickest way out, quickest way wins  ) () ("
    print "        ( :: )      Never disclose, never betray     ( :: )"
    print "        | :: |   Cease to speak or cease to breath   | :: |"
    print "        | )( |        And when you kill a man,       | )( |"
    print "        | || |          you're a murderer            | || |"
    print "        | || |             Kill many                 | || |"
    print "        | || |        and you're a conqueror         | || |"
    print "        | || |        Kill them all ... Ooh..        | || |"
    print "        | || |           Oh you're a God!            | || |"
    print "        ( () )                       -Megadeth       ( () )"
    print "         \  /                                         \  /"
    print "          \/                                           \/"
    
main()


