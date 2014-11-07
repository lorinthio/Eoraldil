import libtcodpy as libtcod
from MapObject import *

class PlayerCamera:
	
	def __init__(self, player, Map, fov_map):
		self.x = player.x
		self.y = player.y
		self.width = 61
		self.height = 41
		self.player = player
		self.Map = Map
		self.fov_map = fov_map
		self.move_camera()
		

	def move_camera(self):
		#global camera_x, camera_y, fov_recompute
		player = self.player
		Map = self.Map
		
		#new camera coordinates (top-left corner of the screen relative to the map)
		x = player.x - (self.width / 2) - 1  #coordinates so that the target is at the center of the screen
		y = player.y - (self.height / 2) - 1
	 
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
		
		dark_offset = libtcod.Color(30, 30, 30)
		
		for y in range(camera.height):
			for x in range(camera.width):
				map_x = camera.x + x
				map_y = camera.y + y
					
				try:
					tile = self.Map.mappedArea[map_x][map_y]
				except:
					tile = Tile(False)
				visible = libtcod.map_is_in_fov(self.fov_map, map_x, map_y)
				
				if visible:
					tile.explored = True
					if tile.explored:
						libtcod.console_set_char_background(con, x, y, tile.color, libtcod.BKGND_SET )
					else:
						libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET )
				else:
					if tile.explored:
						libtcod.console_set_char_background(con, x, y, tile.color - dark_offset, libtcod.BKGND_SET )
					else:
						libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET )
				if y == 0 or y ==camera.height - 1:
					libtcod.console_set_char_background(con, x, y, libtcod.grey, libtcod.BKGND_SET )
				if x == 0 or x ==camera.width - 1:
					libtcod.console_set_char_background(con, x, y, libtcod.grey, libtcod.BKGND_SET )				
		
		for object in objects:
			visible = libtcod.map_is_in_fov(self.fov_map, object.x, object.y)
			if visible:
				if camera.x <= object.x <= (camera.x + camera.width) and camera.y <= object.y <= (camera.y + camera.height):
					tile = self.Map.mappedArea[object.x][object.y]
					if tile.tileType == "leaves":
						pass
					else:
						object.draw(con, camera.x, camera.y)
					
