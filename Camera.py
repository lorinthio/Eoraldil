import libtcodpy as libtcod
from MapObject import *

class PlayerCamera:
	
	def __init__(self, player, Map):
		print("Creating camera!")
		self.x = player.x
		self.y = player.y
		self.width = 81
		self.height = 51
		self.player = player
		self.Map = Map
		self.move_camera()
		

	def move_camera(self):
		#global camera_x, camera_y, fov_recompute
		player = self.player
		Map = self.Map
		
		#new camera coordinates (top-left corner of the screen relative to the map)
		x = player.x - 40  #coordinates so that the target is at the center of the screen
		y = player.y - 25
	 
		#make sure the camera doesn't see outside the map
		if x < 1: x = 1
		if y < 1: y = 1
		if x >= Map.width - self.width - 1: 
			x = Map.width - self.width - 1
		if y >= Map.height - self.height - 1: 
			y = Map.height - self.height - 1
	 
		#if x != camera_x or y != camera_y: fov_recompute = True
		if self.x != x or self.y != y:
			self.x = x
			self.y = y
			return True
		else: return False
		
	
	#def to_camera_coordinates(self, x, y):
		##convert coordinates on the map to coordinates on the screen
		#(x, y) = (x - self.x, y - self.y)
	 
		#if (x < 0 or y < 0 or x >= self.width or y >= self.height):
			#return (None, None)  #if it's outside the view, return nothing
	 
		#return (x, y)
	
	def update(self, console, objects):
		camera_moved = self.move_camera()
		self.draw(console, objects, camera_moved)
	
	def draw(self, con, objects, camera_moved):
		Map = self.Map
		camera = self
		
		
		for y in range(camera.height):
			for x in range(camera.width):
				map_x = camera.x + x
				map_y = camera.y + y
					
				try:
					tile = self.Map.mappedArea[map_x][map_y]
				except:
					tile = Tile(False)
					
				if tile.blocked:
					libtcod.console_set_char_background(con, x, y, Map.wall_color, libtcod.BKGND_SET )
				elif tile.tileType == "water":
					libtcod.console_set_char_background(con, x, y, libtcod.Color(77,163,220), libtcod.BKGND_SET)
				elif not tile.blocked:
					libtcod.console_set_char_background(con, x, y, Map.floor_color, libtcod.BKGND_SET )
					
		for object in objects:
			if camera.x <= object.x <= (camera.x + camera.width) and camera.y <= object.y <= (camera.y + camera.height):
				object.draw(con, camera.x, camera.y)