from random import *
from Character import *
from Item import *
from Monster import *
from MapObject import *
from Camera import *
from GUI import *
import sys
import libtcodpy as libtcod


def main():
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
	player = Player("Lorinthio")
	player.createPlayer()
	player.equipClass("Warrior")
		
	#GUI	
	gui = GUIHandler(player)
	gui.update
	libtcod.console_flush()		
		
	#Generates the map
	local_map = Map(gui, "forest")
	(startx, starty) = local_map.starting_point
	
	#Starts mobHandler and spawns a mob at a random spot
	local_map_objects = [player]
	
	MH = MonsterHandler()
	for i in range(50):
		mob = MH.spawnMonster("Cave")
		mob.spawn(local_map)
		#mob.setTarget(player)
		local_map_objects.append(mob)
	
	#Sets player to the location given from the starting point
	player.x = startx
	player.y = starty
	
	#FOV
	FOV_ALGO = 0
	FOV_LIGHT_WALLS = True
	TORCH_RADIUS = local_map.fov_range
	

	
	fov_map = libtcod.map_new(local_map.width, local_map.height)
	for y in range(local_map.height):
	    for x in range(local_map.width):
		libtcod.map_set_properties(fov_map, x, y, not local_map.mappedArea[x][y].block_sight, not local_map.mappedArea[x][y].blocked)
	
	camera = PlayerCamera(player, local_map, fov_map)
	player.camera = camera
	camera.move_camera()
	
	#Holds current area objects (while be iteratted based on local chunks and objects those chunks hold)
	
	
	#makeMonsters()
	
	#dropItem(30, 30, local_map_objects)

	fov_recompute = True
	
	while not libtcod.console_is_window_closed():
	#handle keys and exit game if needed
		if fov_recompute:
			#recompute FOV if needed (the player moved or something)
			fov_recompute = False
			libtcod.map_compute_fov(fov_map, player.x, player.y, local_map.fov_range, FOV_LIGHT_WALLS, FOV_ALGO)		
		
		(exit, fov_recompute, changeMap, fov_Map) = handle_keys(player, local_map, local_map_objects, gui)
		if changeMap is not None:
			local_map = changeMap
			fov_map = fov_Map
		if exit:
			break
		

		#for object in local_map_objects:
			#if isinstance(object, Monster):
				#object.takeAction(local_map, local_map_objects)
		
		render(con, local_map_objects, player, gui)
		
		libtcod.console_blit(con, 0, 0, camera.width, camera.height, 0, 0, 0)
		libtcod.console_flush()		
		
		for object in local_map_objects:
			object.clear(con, camera.x, camera.y)
			

def render(con, objects, player, gui):	
	camera = player.camera
	camera.update(con, objects)
	gui.update()


def handle_keys(player, local_Map, objects, gui):
	#movement keys
	key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
	x = 0
	y = 0
	fov_recompute = False
	mapChange = False
	if key.vk == libtcod.KEY_CHAR:
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
		elif key.c == ord('c'):
		    gui.activeSide = gui.character
		elif key.c == ord('i'):
		    gui.activeSide = gui.inventory
		    
		#Misc
		elif key.c == ord("n"):
			(local_Map, fov_Map) = newMap(player, gui)
			fov_recompute = True
			mapChange = True			
	
	if not mapChange:
		if fov_recompute:
			player.move(x, y, local_Map, objects)
	if key.vk == libtcod.KEY_ENTER and key.lalt:
	    #Alt+Enter: toggle fullscreen
	    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
     
	elif key.vk == libtcod.KEY_ESCAPE:
	    return (True, fov_recompute, None, None)  #exit game
	
	if not mapChange:	
		return(False, fov_recompute, None, None)
	else:
		return(False, fov_recompute, local_Map, fov_Map)

def newMap(player, gui):
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

def dropItem(x, y, objects):
	#Currently creates the ItemHandler, but later this will be in the server file
	IH = createItems()
	
	#generates an item at level 1
	item = IH.genItem(1)

	#creates an item drop item
	ID = ItemDrop(x, y, item)
	
	#adds to the client side list of objects
	objects.insert(0, ID)


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
	
main()
