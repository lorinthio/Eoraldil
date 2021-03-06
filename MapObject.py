# -*- coding: utf-8 -*-
from random import *
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod
from Object import *
from ObjectAi import *
from Monster import *
from thread import *

#types
# - small dungeon = low number of small rooms
# - cave = cave like area with rivers

class Region:
    
    def __init__(self, MH, mapType="", location=(0, 0)):
        self.Map = Map(None, mapType)
        print "Generated new region at", location
        self.active = False
        self.explored = False
        self.location = location
        
        #For future spawning
        self.MH = MH
        
        #For initial map fill
        self.entityCount = 0
        self.mobs = self.spawnCreatures(MH)
        self.players = []
        self.objects = self.mobs + self.players
        
    def addPlayer(self, player, server):
        if len(self.players) == 0:
            self.active = True
            if not self.explored:
                self.explored = True
                #Check to generate surrounding...
                
                #Check North
                northlocation = (self.location[0], self.location[1] + 1)
                north = server.checkRegion(northlocation)
                if not north:
                    t = start_new_thread(server.makeRegion, (northlocation,))
                    
                #Check East
                eastlocation = (self.location[0] + 1, self.location[1])
                east = server.checkRegion(eastlocation)
                if not east:
                    t = start_new_thread(server.makeRegion, (eastlocation,))
                    
                #Check South
                southlocation = (self.location[0], self.location[1] - 1)
                south = server.checkRegion(southlocation)
                if not south:
                    t = start_new_thread(server.makeRegion, (southlocation,))
                    
                #Check West
                westlocation = (self.location[0] - 1, self.location[1])
                west = server.checkRegion(westlocation)
                if not west:
                    t = start_new_thread(server.makeRegion, (westlocation,))
                
                
        self.players.append(player.object)
        self.objects = self.mobs + self.players
        
    def removePlayer(self, player):
        if player.object in self.players:
            #if p.address == player:
            self.players.remove(player.object)
        
        #If the region is empty then deativate it
        if len(self.players) == 0:
            self.active = False
            self.save()
        
    def save(self):
        # for when we start saving region states
        pass
        
    def spawnCreatures(self, MH):
        mobs = []
        for i in range(30):
            mob = MH.spawnMonster(self.Map)
            if mob != None:
                mob.ID = self.entityCount
                mobs.append(mob)
                self.entityCount += 1
        return mobs       
        

class Map:

    def __init__(self, gui=None, mapType="", mappedArea=None):
        self.gui = gui
        if gui is not None:
            self.messenger = gui.messenger        
        self.mapType = mapType
        self.rooms = []
        self.entities = []
        if mappedArea == None:
            self.generate_map()
        else:
            self.mappedArea = mappedArea
        self.fov_range = self.fovFind()
        self.fov_map = libtcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.map_set_properties(self.fov_map, x, y, not self.mappedArea[x][y].block_sight, not self.mappedArea[x][y].blocked)
        
        
    def fovFind(self):
        if self.mapType == "smalldungeon":
            return 15
        elif self.mapType == "plains":
            return 20 
        elif self.mapType == "cave":
            return 12
        elif self.mapType == "forest":
            return 18
        elif self.mapType == "desert":
            return 20
        elif self.mapType == "fullmap":
            return 1

    def empty_map(self):
        #fill map with "blocked" tiles first
        mapped = [[Tile(False)
            for y in range(self.height)]
                for x in range(self.width)]
        return mapped

    def map_to_chunks(self):
        print("Turning the map to chunks...")
        count = 0
        width = self.width // 16
        widthremain = self.width % 16
        if widthremain > 0:
            width += 1
            widthremain = widthremain / 2
        height = self.height // 16
        heightremain = self.height % 16
        if heightremain > 0:
            height += 1
            heightremain = heightremain / 2
            

        total = width * height
        count = 0
        current = 0.1
        for x in range(width):
            current -= (1.00/width)
            if current <= 0:
                current += 0.1
                count += 1
                print(str(count * 10) + "% complete")
            for y in range(height):
                for chunkx in range(16):
                    for chunky in range(16):
                        mapx = int(x*16 + chunkx - widthremain)
                        mapy = int(y*16 + chunky - heightremain)
                        #print(mapx, mapy)
                        chunk = Chunk(self, x, y)
                        try:
                            chunk.tiles[chunkx][chunky].blocked = self.mappedArea[mapx][mapy].blocked
                            chunk.tiles[chunkx][chunky].block_sight = self.mappedArea[mapx][mapy].block_sight
                        except IndexError:
                            chunk.tiles[chunkx][chunky].blocked = True
                            chunk.tiles[chunkx][chunky].block_sight = True

    def fill_map(self, color):
        #fill map with "blocked" tiles first
        mapped = [[Tile(True)
            for y in range(self.height)]
                for x in range(self.width)]
        for y in range(self.height):
            for x in range(self.width):
                tile = Tile(True)
                tile.color = color
                mapped[x][y] = tile
        
        return mapped

    ### ENTITY GENERATION

    def place_monsters(self, room, maxMobs):
        #choose random number of monsters
        num_monsters = libtcod.random_get_int(0, 0, maxMobs)

        for i in range(num_monsters):
            #choose random spot for this monster
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

            if libtcod.random_get_int(0, 0, 100) < 70:  #70% chance of kobold
                #create an kobold
                Str = random.randint(1,3)
                Con = random.randint(1,3)
                Dex = random.randint(1,3)
                Agi = random.randint(1,3)
                Wis = random.randint(1,3)
                Int = random.randint(1,3)
                chars = Monsters.Monster('small', 10 + Str, 10 + Con, 13 + Dex, 13 + Agi, 8 + Wis, 8 + Int, 'kobold')
                monster = Object.Object(x, y, 'k', libtcod.desaturated_green, True)
                chars.owner = monster
                monster.giveStats(chars)
                monster.setAi(ObjectAis.BasicMonster)
                monster.name = "Kobold"

            else:
                #create an orc
                monster = Object.Object(x, y, 'o', libtcod.darker_green, True)
                Str = random.randint(1,3)
                Con = random.randint(1,3)
                Dex = random.randint(1,3)
                Agi = random.randint(1,3)
                Wis = random.randint(1,3)
                Int = random.randint(1,3)
                chars = Monsters.Monster('medium', 13 + Str, 12 + Con, 9 + Dex, 9 + Agi, 10 + Wis, 8 + Int, 'orc')
                chars.owner = monster
                monster.giveStats(chars)
                monster.setAi(ObjectAis.BasicMonster)
                monster.name = "Orc"

            self.entities.append(monster)

    ### MAP GENERATION

    def generate_map(self):
        # if no maptype given, then pick one
        if self.mapType == "":
            mapTypes = ["smalldungeon", "cave", "forest"] #desert
            self.mapType = choice(mapTypes)
            
            
        # Generate for the maptype
        if self.mapType == "smalldungeon":
            self.generate_small_dungeon()
        elif self.mapType == "cave":
            self.generate_cave()
        elif self.mapType == "forest":
            self.generate_forest() 
        elif self.mapType == "desert":
            self.generate_desert() 
            
        
        elif self.mapType == "fullmap":
            self.width = 20
            self.height = 20
            self.mappedArea = self.fill_map(libtcod.black)
            self.starting_point = (1, 1)

    def generate_desert(self):
        if self.gui is not None:
            self.messenger.message("Generating Forest", libtcod.yellow)
            self.gui.update()
        libtcod.console_flush()	
        self.width = randint(120, 360)
        self.height = randint(80, 240)
        
        self.wall_color = libtcod.Color(117, 98, 36)
        self.floor_color = libtcod.Color(206, 186, 118)

        self.mappedArea = self.empty_map()
        
        self.setupCellularDesert()
        for i in range(6):
            if self.gui is not None:
                self.messenger.message(str(i * 20) + "%")
                self.gui.update()
                libtcod.console_flush()	
            self.automate()
        self.generateDepth()
        self.colorMap()
        self.randomStartPoint()
        #self.place_trees()
        if self.gui is not None:
            self.messenger.message("Map finished generating!", libtcod.yellow)
            self.gui.update()        
            libtcod.console_flush()

    def generate_small_dungeon(self):
        self.width = randint(70, 110)
        self.height = randint(40, 60)

        self.wall_color = libtcod.Color(50, 50, 50)
        self.floor_color = libtcod.Color(120, 120, 120)
        
        self.mappedArea = self.fill_map(self.wall_color)

        room_max_size = 10
        room_min_size = 5
        max_rooms = 10
        num_rooms = 0
        failedCount = 0
        while failedCount <= 10:
            w = libtcod.random_get_int(0, room_min_size, room_max_size)
            h = libtcod.random_get_int(0, room_min_size, room_max_size)
            x = libtcod.random_get_int(0, 0, self.width - w - 1)
            y = libtcod.random_get_int(0, 0, self.height - h - 1)

            # test the new room in the map
            new_room = RectRoom(x, y, w, h)
            failed = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break

            # if the room passes, then put it in
            if not failed:
                newroom = self.create_room(new_room)

                if num_rooms == 0:
                    self.starting_point = newroom.center()

                (new_x, new_y) = newroom.center()

                #all rooms after the first:
                #connect it to the previous room with a tunnel

                #center coordinates of previous room
                (prev_x, prev_y) = self.rooms[num_rooms - 1].center()

                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    self.create_h_tunnel(prev_x, new_x, prev_y)
                    self.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    self.create_v_tunnel(prev_y, new_y, prev_x)
                    self.create_h_tunnel(prev_x, new_x, new_y)
                    
                #finally, append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1                
            else:
                failedCount += 1
                



    def create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        self.rooms.append(room)
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tile = self.mappedArea[x][y]
                tile.blocked = False
                tile.block_sight = False
                tile.color = self.floor_color

        # GENERATE ENTITIES IN THIS ROOM
        #if self.mapType == "smalldungeon":
            #self.place_monsters(room, 2)
        return room

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tile = self.mappedArea[x][y]
            tile.blocked = False
            tile.block_sight = False
            tile.color = self.floor_color

    def create_v_tunnel(self, y1, y2, x):
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tile = self.mappedArea[x][y]
            tile.blocked = False
            tile.block_sight = False
            tile.color = self.floor_color

    def generate_forest(self):
        if self.gui is not None:
            self.messenger.message("Generating Forest", libtcod.yellow)
            self.gui.update()
        libtcod.console_flush()	
        self.width = randint(80, 300) # 100, 300
        self.height = randint(50, 180) # 60, 180
        
        self.wall_color = libtcod.Color(214, 138, 84)
        self.floor_color = libtcod.Color(90, 205, 78)

        self.mappedArea = self.fill_map(self.wall_color)
        
        self.setupCellular()
        for i in range(6):
            if self.gui is not None:
                self.messenger.message(str(i * 15) + "%")
                self.gui.update()
                libtcod.console_flush()	
            self.automate()
        self.generateDepth()
        self.colorMap()
        self.randomStartPoint()
        self.place_trees()
        if self.gui is not None:
            self.messenger.message("Map finished generating!", libtcod.yellow)
            self.gui.update()        
            libtcod.console_flush()	

    def place_trees(self):
        if self.mapType == "forest":
            leaves = libtcod.darker_green
            stump = libtcod.dark_sepia
            ##     Shape 1
            ##       #
            ##      ###
            ##       #
            
            ##     Shape 2
            ##       #
            ##      ###
            ##      ###
            ##       #  
            
            trees = (self.width * self.height) / 50
            
            for i in range(trees):
                (posx, posy) = self.randomPoint()
                #make stump
                tile = self.mappedArea[posx][posy]
                tile.color = stump
                tile.blocked = True
                tile.block_sight = True
                #make leaves
                self.makeLeaf(posx+1, posy-1, leaves)
                self.makeLeaf(posx, posy-1, leaves)
                self.makeLeaf(posx-1, posy-1, leaves)
                self.makeLeaf(posx+1, posy-2, leaves)
                self.makeLeaf(posx, posy-2, leaves)
                self.makeLeaf(posx-1, posy-2, leaves)                
                self.makeLeaf(posx, posy-3, leaves)
                if randint(0,4) >= 3:
                    #make bigger tree
                    self.makeLeaf(posx-1, posy-3, leaves)
                    self.makeLeaf(posx+1, posy-3, leaves)
                    self.makeLeaf(posx, posy-4, leaves)
                    
            
    def makeLeaf(self, posx, posy, color):
        tile = self.mappedArea[posx][posy]
        tile.color = color
        tile.blocked = False
        tile.block_sight = False
        tile.tileType = "leaves"        
            
            

    # cave generation code!
    def generate_cave(self):
        if self.gui is not None:
            self.messenger.message("Generating Cave", libtcod.yellow)
            self.gui.update()
            libtcod.console_flush()	
        self.width = randint(120, 200)
        self.height = randint(40, 100)
        
        self.wall_color = libtcod.Color(98, 54, 35)
        self.floor_color = libtcod.Color(112, 86, 75)
        
        self.mappedArea = self.fill_map(self.wall_color)

        self.setupCellular()
        for i in range(4):
            if self.gui is not None:
                self.messenger.message(str(i * 20) + "%")
                self.gui.update()
                libtcod.console_flush()	
            self.automate()
        self.generateDepth()
        if self.gui is not None:
            self.messenger.message("75%")
            self.gui.update()
            libtcod.console_flush()	
        self.colorMap()
        self.randomStartPoint()
        if self.gui is not None:
            self.messenger.message("Map finished generating", libtcod.yellow)
            self.gui.update()
            libtcod.console_flush()	

    def colorMap(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.mappedArea[x][y]
                if tile.blocked:
                    tile.height = 0
                    tile.color = self.wall_color
                elif tile.tileType == "water" or tile.tileType== "leaves":
                    pass
                else:
                    tile.color = self.floor_color
                    if "forest" in self.mapType or "cave" in self.mapType:
                        height = tile.height - 10
                        if height < 0:
                            height = abs(height)
                            tile.color = self.floor_color - libtcod.Color(5 * height, 5 * height, 5 * height)
                        elif height > 0:
                            tile.color = self.floor_color + libtcod.Color(5 * height, 5 * height, 5 * height)

    def randomStartPoint(self):
        pointfound = False
        while not pointfound:
            posx = randint(2, self.width-2)
            posy = randint(2, self.height-2)
            if not self.mappedArea[posx][posy].blocked:
                break
        self.starting_point = (posx, posy)
        
    def randomSpawnPoint(self, spawned_mob):
        mobs = self.entities
        pointfound = False
        ignoredTiles = ["water", "leaves"]
        while not pointfound:
            posx = randint(2, self.width-2)
            posy = randint(2, self.height-2)
            if not self.mappedArea[posx][posy].blocked:
                if self.mappedArea[posx][posy].tileType not in ignoredTiles:
                    Blocked = False
                    for mob in mobs:
                        if mob.x == posx and mob.y == posy:
                            Blocked = True
                    if not Blocked:
                        mobs.append(spawned_mob)
                        break
                    
        return (posx, posy) 
    
    def randomPoint(self):
        mobs = self.entities
        pointfound = False
        ignoredTiles = ["water", "leaves"]
        while not pointfound:
            posx = randint(2, self.width-2)
            posy = randint(2, self.height-2)
            if not self.mappedArea[posx][posy].blocked:
                if self.mappedArea[posx][posy].tileType not in ignoredTiles:
                    break
                    
        return (posx, posy)  

    def setupCellularDesert(self):
        self.temp_map = self.fill_map(self.wall_color)
        ##Fill the map with ground at the specified percentage
        ##Lower numbers make more open caves, while higher numbers result in more closed in, but more un connected 'rooms'
        ##40% is a decent percentage
        rCheck = 70
        
        #Left border
        for x in range(2, 10):
            for y in range(2,self.height-2):
                r = randint(1,100)
                if rCheck < r:
                    self.mappedArea[x][y].color = self.floor_color
                    self.mappedArea[x][y].blocked = False
                    self.mappedArea[x][y].block_sight = False
                else:
                    self.mappedArea[x][y].color = self.wall_color
                    self.mappedArea[x][y].blocked = True
                    self.mappedArea[x][y].block_sight = True
                    
        #Right border
        for x in range(self.width - 10, self.width):
            for y in range(2,self.height-2):
                r = randint(1,100)
                if rCheck < r:
                    self.mappedArea[x][y].color = self.floor_color
                    self.mappedArea[x][y].blocked = False
                    self.mappedArea[x][y].block_sight = False
                else:
                    self.mappedArea[x][y].color = self.wall_color
                    self.mappedArea[x][y].blocked = True
                    self.mappedArea[x][y].block_sight = True
        
        #Top border
        for x in range(2,self.width-2):
            for y in range(2,10):
                r = randint(1,100)
                if rCheck < r:
                    self.mappedArea[x][y].color = self.floor_color
                    self.mappedArea[x][y].blocked = False
                    self.mappedArea[x][y].block_sight = False
                else:
                    self.mappedArea[x][y].color = self.wall_color
                    self.mappedArea[x][y].blocked = True
                    self.mappedArea[x][y].block_sight = True
                    
        #Bottom border
        for x in range(2,self.width-2):
            for y in range(self.height - 10, self.height - 2):
                r = randint(1,100)
                if rCheck < r:
                    self.mappedArea[x][y].color = self.floor_color
                    self.mappedArea[x][y].blocked = False
                    self.mappedArea[x][y].block_sight = False
                else:
                    self.mappedArea[x][y].color = self.wall_color
                    self.mappedArea[x][y].blocked = True
                    self.mappedArea[x][y].block_sight = True
                
    def setupCellular(self):
        self.temp_map = self.fill_map(self.wall_color)
        ##Fill the map with ground at the specified percentage
        ##Lower numbers make more open caves, while higher numbers result in more closed in, but more un connected 'rooms'
        ##40% is a decent percentage
        if self.mapType == "forest":
            rCheck = 34
        elif self.mapType == "cave":
            rCheck = 38
        
        for x in range(2,self.width-2):
            for y in range(2,self.height-2):
                r = randint(1,100)
                if rCheck < r:
                    self.mappedArea[x][y].color = self.floor_color
                    self.mappedArea[x][y].blocked = False
                    self.mappedArea[x][y].block_sight = False
                else:
                    self.mappedArea[x][y].color = self.wall_color
                    self.mappedArea[x][y].blocked = True
                    self.mappedArea[x][y].block_sight = True

    def automate(self):
        ##Go through each cell to see if it needs to be transformed
        for x in range(2, (self.width - 2)):
            for y in range(2,(self.height - 2)):
                self.checkCell(x,y)
                #self.mappedArea[x][y] = cell
                # self.temp_map[x][y] = cell

    def checkCell(self,x,y):
        walls = 0
        ##Check in a 3x3 area around the chosen cell
        for x2 in range(0,3):
            for y2 in range(0,3):
                posX = x2 + x - 1
                posY = y2 + y - 1
                if self.mappedArea[posX][posY].blocked:
                    walls+=1 ##Has an offset to get closer to the wall
    ##If there are 5 or more wall segments next to a piece of floor
        ##Turn it into a wall
        if not self.mappedArea[x][y].blocked:
            if walls >= 5:
                self.mappedArea[x][y].blocked = True
                self.mappedArea[x][y].block_sight = True
                return
            else:
                self.mappedArea[x][y].blocked = False
                self.mappedArea[x][y].block_sight = False
                return
        ##If there are 4 or more wall segments next to another wall
        ##Keep it a wall, otherwise turn it into floor
        if self.mappedArea[x][y].blocked:
            if walls >= 4:
                self.mappedArea[x][y].blocked = True
                self.mappedArea[x][y].block_sight = True
                return
            else:
                self.mappedArea[x][y].blocked = False
                self.mappedArea[x][y].block_sight = False
                return

    def generateDepth(self):
        #noise_octaves = 4.0
        noise_zoom = 2.0
        noise_hurst = libtcod.NOISE_DEFAULT_HURST
        noise_lacunarity = libtcod.NOISE_DEFAULT_LACUNARITY

        mapped = self.mappedArea
        
        water_color = libtcod.sky

        if self.mapType == "desert":
            water_level = 0.04
        else:
            water_level = 0.07

        noise = libtcod.noise_new(2, noise_hurst, noise_lacunarity)
        for y in range(self.height):
                for x in range(self.width):
                    f = [noise_zoom * x / (self.width), noise_zoom * y / (self.height)]
                    noisefloat = abs(libtcod.noise_get(noise, f, libtcod.NOISE_PERLIN))
                    if noisefloat >= float(0) and noisefloat <= water_level:
                        tile = mapped[x][y]
                        tile.tileType = "water"
                        tile.blocked = False
                        tile.block_sight = False
                        tile.slows = True
                        #Depth = Color darkness
                        depth = int(10 - (noisefloat * 100))
                        tile.color = water_color - libtcod.Color(5 * depth, 5 * depth, 5 * depth)
                        tile.height = 0 - depth
                    else:
                        tile = mapped[x][y]
                        height = int(noisefloat / 0.03)
                        if height > 12:
                            height = 12
                        tile.height = height

        #Block the edges of the map so player can't crash the game
        for y in range(self.height):
            #mapped[0][y].tileType = None
            mapped[0][y].blocked = True
            mapped[self.width-1][y].blocked = True
        for x in range(self.width):
            mapped[x][0].blocked = True
            mapped[x][self.height-1].blocked = True


class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight=None, tileType=None, color=None):
        self.blocked = blocked
        self.block_sight = block_sight
        self.explored = False
        self.slows = False
        self.tileType = tileType
        self.color = color

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            self.block_sight = blocked

class Chunk:

    def __init__(self, map, posx, posy):
        self.owner = map
        self.tiles = self.empty_chunk()
        self.objects = ()
        self.posx = posx
        self.posy = posy

    def empty_chunk(self):
        #fill map with "blocked" tiles first
        mapped = [[Tile(False)
            for y in range(16)]
                for x in range(16)]
        return mapped

class RectRoom:

    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersects(self, other):
        #returns true if this rectangle intersects with another one
        if self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1:
            return True
        else:
            return False
