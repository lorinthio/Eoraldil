from random import *
from Character import *
from Item import *
from Monster import *
from MapObject import *
<<<<<<< HEAD
from Camera import *
=======
>>>>>>> origin/master
import libtcodpy as libtcod


def main():
	player = Player("Lorinthio")
	player.createPlayer()
	player.equipClass("Warrior")
	
	local_map = Map("cave")
	(startx, starty) = local_map.starting_point
	
	player.x = startx
	player.y = starty
	
<<<<<<< HEAD
	
	camera = PlayerCamera(player, local_map)
=======
	print(player.x, player.y)
	
	camera = PlayerCamera(player.x, player.y, player, local_map)
>>>>>>> origin/master
	
	player.camera = camera
	camera.move_camera()
	
<<<<<<< HEAD
=======
	print(camera.x, camera.y)
	
>>>>>>> origin/master
	#Holds current area objects (while be iteratted based on local chunks and objects those chunks hold)
	local_map_objects = [player]
	
	#makeMonsters()
	
<<<<<<< HEAD
	SCREEN_W = 81
	SCREEN_H = 51
	LIMIT_FPS = 30
	
	print("Instantiating libtcod")
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(SCREEN_W, SCREEN_H, 'Eoraldil', False)
	libtcod.sys_set_fps(LIMIT_FPS)
	
	print("making the window")
	con = libtcod.console_new(SCREEN_W, SCREEN_H)
	#dropItem(30, 30, local_map_objects)
	
	print("starting render")
	while not libtcod.console_is_window_closed():
	#handle keys and exit game if needed
		exit = handle_keys(player, local_map, local_map_objects)
		if exit:
			break	
		
		render(con, local_map_objects, player)
		
		libtcod.console_blit(con, 0, 0, SCREEN_W, SCREEN_H, 0, 0, 0)
		libtcod.console_flush()
		
		for object in local_map_objects:
			object.clear(con, camera.x, camera.y)

=======
	SCREEN_W = 80
	SCREEN_H = 50
	LIMIT_FPS = 30
	
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(SCREEN_W, SCREEN_H, 'Eoraldil', False)
	libtcod.sys_set_fps(LIMIT_FPS)
	con = libtcod.console_new(SCREEN_W, SCREEN_H)
	camera.move_camera()
	dropItem(30, 30, local_map_objects)
	
	while not libtcod.console_is_window_closed():
	    render(con, local_map_objects, player)
	
	    libtcod.console_blit(con, 0, 0, SCREEN_W, SCREEN_H, 0, 0, 0)
	    libtcod.console_flush()
	
	    for object in local_map_objects:
		object.clear(con)
		    
	    #handle keys and exit game if needed
	    exit = handle_keys(player, local_map, local_map_objects)
	    if exit:
		break

class PlayerCamera:
	
	def __init__(self, x, y, player, Map):
		self.x = x
		self.width = 80
		self.height = 50
		self.y = y
		self.player = player
		self.Map = Map

	def move_camera(self):
		#global camera_x, camera_y, fov_recompute
		player = self.player
		Map = self.Map
		
		#new camera coordinates (top-left corner of the screen relative to the map)
		x = player.x - 40  #coordinates so that the target is at the center of the screen
		y = player.y - 25
	 
		#make sure the camera doesn't see outside the map
		if x < 0: x = 0
		if y < 0: y = 0
		if x > Map.width - 80 - 1: x = Map.width - 80 - 1
		if y > Map.height - 50 - 1: y = Map.width - 50 - 1
	 
		#if x != camera_x or y != camera_y: fov_recompute = True
	 
		(self.x, self.y) = (x, y)
	
	def to_camera_coordinates(self, x, y):
		#convert coordinates on the map to coordinates on the screen
		(x, y) = (x - self.x, y - self.y)
	 
		if (x < 0 or y < 0 or x >= self.width or y >= self.height):
			return (None, None)  #if it's outside the view, return nothing
	 
		return (x, y)
	
	def update(self, console, objects):
		self.move_camera()
		self.draw(console, objects)
	
	def draw(self, con, objects):
		Map = self.Map
		camera = self
		
		for y in range(camera.height):
			for x in range(camera.width):
				map_x = camera.x + x
				map_y = camera.y + y
					
				try:
					tile = self.Map.mappedArea[map_x][map_y]
				except:
					tile = Tile(True)
					
				if tile.blocked:
					libtcod.console_set_char_background(con, x, y, Map.wall_color, libtcod.BKGND_SET )
				elif tile.tileType == "water":
					libtcod.console_set_char_background(con, x, y, libtcod.blue, libtcod.BKGND_SET )
				elif not tile.blocked:
					libtcod.console_set_char_background(con, x, y, Map.floor_color, libtcod.BKGND_SET )
					
		for object in objects:
			if camera.x <= object.x <= (camera.x + camera.width) and camera.y <= object.y <= (camera.y + camera.height):
				object.draw(con)		
>>>>>>> origin/master

def render(con, objects, player):	
	camera = player.camera
	camera.update(con, objects)


def handle_keys(player, Map, objects):
	#movement keys
	key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)
	x = 0
	y = 0
	if key.vk == libtcod.KEY_CHAR:
		if key.c == ord('w'):
		    y = -1
		    #print('w')
		elif key.c == ord('s'):
		    y = 1
		    #print('s')
		elif key.c == ord('a'):
		    x = -1
		    #print('a')
		elif key.c == ord('d'):
		    x = 1
		    #print('d')
	player.move(x, y, Map, objects)
	if key.vk == libtcod.KEY_ENTER and key.lalt:
	    #Alt+Enter: toggle fullscreen
	    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
     
	elif key.vk == libtcod.KEY_ESCAPE:
	    return True  #exit game		


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
