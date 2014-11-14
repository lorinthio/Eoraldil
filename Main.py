from random import *
from Character import *
from Item import *
from Monster import *
from MapObject import *
from Camera import *
from GUI import *
import sys
import winsound
from Client import *
import wave
import thread
import libtcodpy as libtcod


def main():
    setrecursionlimit(3500)
    #Window
    SCREEN_W = 81
    SCREEN_H = 51
    LIMIT_FPS = 30

    #Make Libtcod Available
    print("Instantiating libtcod")
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_W, SCREEN_H, 'Eoraldil', False)
    libtcod.sys_set_fps(LIMIT_FPS)

    con = libtcod.console_new(SCREEN_W, SCREEN_H)

    #Default Character fill in
    player = Player("Lorinthio Shivst")
    #player = Player("Phrixious")
    player.createPlayer()
    player.equipClass("Warrior")

    local_map_objects = []
    local_mobs = {}

    #GUI
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
    gui = GUIHandler(player)
    gui.update()
    libtcod.console_flush()

    #Generates the map
    local_map = Map(gui, "fullmap")
    (startx, starty) = local_map.starting_point

    #Sets player to the location given from the starting point
    player.x = startx
    player.y = starty

    local_players = [player]

    #FOV
    FOV_ALGO = 0
    FOV_LIGHT_WALLS = True
    TORCH_RADIUS = 12

    fov_map = libtcod.map_new(local_map.width, local_map.height)
    for y in range(local_map.height):
        for x in range(local_map.width):
            libtcod.map_set_properties(fov_map, x, y, not local_map.mappedArea[x][y].block_sight, not local_map.mappedArea[x][y].blocked)

    camera = PlayerCamera(player, local_map, fov_map)
    player.camera = camera
    camera.move_camera()

    #gui.update()
    #libtcod.console_flush()

    #CLIENT
    host = "localhost"
    port = "25565"
    c = Client(host, int(port), player, gui)

    fov_recompute = True

    music = thread.start_new_thread(play_music, ('forest',))
    
    timer = Timer()
    frame = 0
    
    while not libtcod.console_is_window_closed():
        
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
        #handle keys and exit game if needed
        if fov_recompute:
            #recompute FOV if needed (the player moved or something)
            fov_recompute = False
            libtcod.map_compute_fov(fov_map, player.x, player.y, local_map.fov_range, FOV_LIGHT_WALLS, FOV_ALGO)

            c.send_loc = True

        c.Loop()

        (local_players, local_map_objects, local_mobs) = checkClient(c, local_players, local_map_objects, local_mobs)

        #Check if server changed the map, or player changed zones
        if c.mapChange:
            c.mapChange = False
            (local_map, fov_Map) =  makeMapFromServer(player, gui, local_map, c)
            fov_recompute = True
            fov_map = fov_Map

        objects = local_map_objects + local_players
        if not fov_recompute:

            (exit, fov_recompute, changeMap, fov_Map) = handle_keys(player, local_map, objects, gui, key)

            if changeMap is not None:
                local_map = changeMap
                fov_map = fov_Map

            if exit:
                try:
                    thread.exit()
                except:
                    sys.exit()

        #for object in local_map_objects:
            #if isinstance(object, Monster):
                #object.takeAction(local_map, local_map_objects)

        render(con, local_map_objects + local_players, player, gui, mouse)

        libtcod.console_blit(con, 0, 0, camera.width, camera.height, 0, 0, 0)
        libtcod.console_flush()

        for object in objects:
            object.clear(con, camera.x, camera.y)
            
        frame = timer.nextFrame()
        gui.fps = (1 / frame) // 1

    

def play_music(musicname):
    path = ".//Audio/" + musicname + ".wav"
    while True:
        winsound.PlaySound(path, winsound.SND_LOOP)

def play_sound(soundname):
    path = ".//Audio/" + soundname + ".wav"

def render(con, objects, player, gui, mouse):
    camera = player.camera
    camera.update(con, objects)
    gui.update(objects, mouse)


def handle_keys(player, local_Map, objects, gui, key):
    #movement keys
    x = 0
    y = 0
    fov_recompute = False
    mapChange = False
    if player.typing:
        typeHandler(key, gui)
    if key.vk == libtcod.KEY_CHAR:
        if player.typing:
            pass # Ignore this block
        else:
            #Movement
            if key.c == ord('w'):
                y = -1
                fov_recompute = True
                #print('w')
            elif key.c == ord('s'):
                y = 1
                fov_recompute = True
                #print('s')
            elif key.c == ord('a'):
                x = -1
                fov_recompute = True
                #print('a')
            elif key.c == ord('d'):
                x = 1
                fov_recompute = True
                #print('d')
    
            #Side Windows
            elif key.c == ord('p'):
                gui.activeSide = gui.character
            elif key.c == ord('o'):
                gui.activeSide = gui.equipment
            elif key.c == ord('i'):
                gui.activeSide = gui.inventory
    
            #Action Keys
            elif key.c == ord('e'):
                use_nearby(player, local_Map, objects)
    
    
            #Misc
            elif key.c == ord("n"):
                (local_Map, fov_Map) = newMap(player, gui)
                fov_recompute = True
                mapChange = True



    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ENTER:
        if not player.typing:
            player.typing = True
        else:
            player.typing = False
            gui.entry.endEntry()

    elif key.vk == libtcod.KEY_ESCAPE:
        return (True, fov_recompute, None, None)  #exit game

    if not mapChange:
        if fov_recompute:
            player.move(x, y, local_Map, objects)
        return(False, fov_recompute, None, None)
    else:
        return(False, fov_recompute, local_Map, fov_Map)

def typeHandler(key, gui):
    if key.vk == libtcod.KEY_BACKSPACE:
            gui.entry.removeLetter()
    elif key.vk != 0:
        if key.c != 0:
            gui.entry.addLetter(chr(key.c))

def use_nearby(player, Map, objects):
    print('Tried to use nearby')
    x = player.x
    y = player.y
    for object in objects:
        if x-1 <= object.x <= x+1:
            if y-1 <= object.y <= y+1:
                if object != player:
                    object.use()

def newMap(player, gui, local_Map=None):
    if local_Map == None:
        local_Map = Map(gui)

    (player.x, player.y) = local_Map.starting_point
    player.camera.Map = local_Map
    player.camera.move_camera()
    fov_Map = libtcod.map_new(local_Map.width, local_Map.height)
    for y in range(local_Map.height):
        for x in range(local_Map.width):
            libtcod.map_set_properties(fov_Map, x, y, not local_Map.mappedArea[x][y].block_sight, not local_Map.mappedArea[x][y].blocked)
    libtcod.map_compute_fov(fov_Map, player.x, player.y, local_Map.fov_range, True, 0)

    player.camera.Map = local_Map
    player.camera.fov_map = fov_Map
    player.camera.move_camera()

    return (local_Map, fov_Map)

def makeMapFromServer(player, gui, local_map, c):
    gui.update
    libtcod.console_flush()    
    data = c.mapData
    startpoint = data['startingPoint']
    width = data['width']
    height = data['height']
    fov_range = data['fovRange']
    maptype = data['mapType']

    mapped = [[Tile(False)
        for y in range(height)]
        for x in range(width)]

    while not c.mapDone:
        c.Loop()

    singletile = float(100 * (1 / width))
    count = 0
    i = 0

    for x in range(width):
        count += singletile
        if count >= 10:
            i += 1
            gui.message(str(i * 10) + "% loaded from server", libtcod.yellow)
            gui.update
            libtcod.console_flush()
        chunk = c.chunks[x]
        for y in range(height):
            tileinfo = chunk[str(y)]
            mapped[x][y] = Tile(tileinfo[0], tileinfo[1], tileinfo[2], libtcod.Color(tileinfo[3][0], tileinfo[3][1], tileinfo[3][2]))

    gui.message("Initializing map", libtcod.yellow)
    gui.update
    libtcod.console_flush()

    newmap = local_map
    newmap.mappedArea = mapped
    newmap.width = width
    newmap.height = height
    newmap.fov_range = fov_range
    newmap.starting_point = startpoint

    (player.x, player.y) = newmap.starting_point

    fov_Map = libtcod.map_new(newmap.width, newmap.height)

    for y in range(newmap.height):
        for x in range(newmap.width):
            libtcod.map_set_properties(fov_Map, x, y, not newmap.mappedArea[x][y].block_sight, not newmap.mappedArea[x][y].blocked)

    libtcod.map_compute_fov(fov_Map, player.x, player.y, newmap.fov_range, True, 0)

    player.camera.Map = newmap
    player.camera.fov_map = fov_Map
    player.camera.move_camera()

    return (newmap, fov_Map)


#def dropItem(x, y, objects):
    ##Currently creates the ItemHandler, but later this will be in the server file
    #IH = createItems()

    ##generates an item at level 1
    #item = IH.genItem(1)

    ##creates an item drop item
    #ID = ItemDrop(x, y, item)

    ##adds to the client side list of objects
    #objects.insert(0, ID)

def checkClient(c, local_players, local_objects, local_mobs):
    #Check for moved players
    for name in c.moved_players:
        if name in c.removed_players:
            for player in local_players:
                if player.name == name:
                    print("removing " + player.name)
                    local_players.remove(player)
        else:
            found = False
            for local_play in local_players:
                if local_play.name == name:
                    found = True
                    pos = c.moved_players[name]
                    local_play.put(pos[0], pos[1])
            if not found:
                newplayer = Player(name)
                pos = c.moved_players[name]
                newplayer.put(pos[0], pos[1])
                local_players.append(newplayer)
    c.moved_players = {}

    for mob in c.spawnedMobs:
        pos = mob['position']
        color = libtcod.Color(mob['color'][0], mob['color'][1], mob['color'][2])
        created_mob = EntityObject(pos[0], pos[1], mob['char'], color, True)
        created_mob.name = mob['name']
        created_mob.ID = mob['id']
        local_objects.append(created_mob)
        local_mobs[created_mob.ID] = created_mob
    c.spawnedMobs = []
        
    if c.movedMobs != None:
        movedmobs = c.movedMobs['mobinfo']
        for ID in movedmobs:
            localmob = local_mobs[ID]
            localmob.x = movedmobs[ID][0]
            localmob.y = movedmobs[ID][1] 
        c.movedMobs = None
    
    for name in c.removed_players:
        for player in local_players:
            if player.name == name:
                #print("removing " + player.name)
                local_players.remove(player)
    c.removed_players = []
    
    return (local_players, local_objects, local_mobs)
    

#Initial creation of character with prompts to test each class easily
def chooseClass():
    print("Please select a class:")
    print("- Warrior")
    print("- Rogue")
    print("- Cleric")
    print("- Mage")

    choice = input("Class : ")
    player = None # Instantiates no other use really
    if choice[0] == "w":
        print("You have selected Warrior")
        player = Warrior()
    elif choice[0] == "r":
        print("You have selected Rogue")
        player = Rogue()
    elif choice[0] == "c":
        print("You have selected Cleric")
        player = Cleric()
    elif choice[0] == "m":
        print("You have selected Mage")
        player = Mage()
    else:
        print("invalid choice please try again")
        player = chooseClass() # If it fails it will repeat this code until a suitable answer is given

    return player

class Timer:
    
    def __init__(self):
        self.curTime = time.time()
        
    def nextFrame(self):
        frame = time.time() - self.curTime
        self.curTime = time.time()
        
        return frame

main()
