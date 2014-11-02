from random import *
from Character import *
from Item import *
from Monster import *
from MapObject import *
from Camera import *
import libtcodpy as libtcod


def main():
	player = Player("Lorinthio")
	player.createPlayer()
	player.equipClass("Warrior")
	
	local_map = Map("cave")
	(startx, starty) = local_map.starting_point
	
	player.x = startx
	player.y = starty
	
	#FOV
	FOV_ALGO = 0
	FOV_LIGHT_WALLS = True
	TORCH_RADIUS = 10
	fov_map = libtcod.map_new(local_map.width, local_map.height)
	for y in range(local_map.height):
	    for x in range(local_map.width):
		libtcod.map_set_properties(fov_map, x, y, not local_map.mappedArea[x][y].block_sight, not local_map.mappedArea[x][y].blocked)	
	
	camera = PlayerCamera(player, local_map, fov_map)
	player.camera = camera
	camera.move_camera()
	
	#Holds current area objects (while be iteratted based on local chunks and objects those chunks hold)
	local_map_objects = [player]
	
	#makeMonsters()

	SCREEN_W = 81
	SCREEN_H = 51
	LIMIT_FPS = 30
	

	
	print("Instantiating libtcod")
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(SCREEN_W, SCREEN_H, 'Eoraldil', False)
	libtcod.sys_set_fps(LIMIT_FPS)
	
	con = libtcod.console_new(SCREEN_W, SCREEN_H)
	#dropItem(30, 30, local_map_objects)
	
	while not libtcod.console_is_window_closed():
	#handle keys and exit game if needed
		(exit, fov_recompute) = handle_keys(player, local_map, local_map_objects)
		if exit:
			break	
		
		if fov_recompute:
			#recompute FOV if needed (the player moved or something)
			fov_recompute = False
			libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)		
		
		render(con, local_map_objects, player)
		
		libtcod.console_blit(con, 0, 0, SCREEN_W, SCREEN_H, 0, 0, 0)
		libtcod.console_flush()
		
		for object in local_map_objects:
			object.clear(con, camera.x, camera.y)

def render(con, objects, player):	
	camera = player.camera
	camera.update(con, objects)


def handle_keys(player, Map, objects):
	#movement keys
	key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
	x = 0
	y = 0
	fov_recompute = False
	if key.vk == libtcod.KEY_CHAR:
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
	player.move(x, y, Map, objects)
	if key.vk == libtcod.KEY_ENTER and key.lalt:
	    #Alt+Enter: toggle fullscreen
	    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
     
	elif key.vk == libtcod.KEY_ESCAPE:
	    return (True, fov_recompute)  #exit game
	
	return(False, fov_recompute)


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


#Simply checks if an object is a type for example if item is a Weapon (Gonna move to a tools module)
def isType(obj, name):
	if name == type(obj).__name__:
		return True
	else:
		return False
	
main()
