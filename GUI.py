import textwrap
import libtcodpy as libtcod

class GUIHandler:
    def __init__(self, player):
	self.gui_panels = []
	self.fps = 30
	self.player = player
	
	#Message Panels
	gui_message = MessagePanel(player, 40, 41, 40, 10)
	gui_message.message("Welcome to Eoraldil!", libtcod.yellow)
	gui_message.message("Your journey begins... ", libtcod.grey)
	self.messenger = gui_message
	
	#Inventory Panel
	inventory = InventoryPanel(player, 62, 0, 19, 39)
	self.inventory = inventory
	
	equipment = EquipmentPanel(player, 62, 0, 19, 39)
	self.equipment = equipment
	
	#Character Panel
	character = CharacterPanel(player, 62, 0, 19, 39)
	self.activeSide = character
	self.character = character
	
	#Vital Panels
	gui_vitals = VitalPanel(player, 0, 41, 30, 9)
	self.gui_panels.append(gui_vitals)	
	
	#gui_fps = FpsCounter(None, 73, 1, 8, 2)
	#self.fpsPanel = gui_fps
	#self.gui_panels.append(gui_fps)
	
	#Mouse Panel
	gui_mouse = MousePanel(player, 0, 49, 40, 2)
	self.MousePanel = gui_mouse
	self.gui_panels.append(gui_mouse)
	
    def message(self, message, color=libtcod.white):
	self.messenger.message(message, color)
	
    
    def update(self, objects=None, mouse=None):
	self.activeSide.update()
	self.messenger.update()	
	for panel in self.gui_panels:
	    if panel is self.MousePanel:
		if objects != None:
		    panel.refresh(objects, mouse)		
	    panel.update()	 
	    
	    
	    #THIS IS FOR FPS TESTING
	    #if panel is self.fpsPanel:
		#panel.setFps(self.fps)


	

#class EntryBar(MessagePanel):
    
    #def __init__(self, gui, player, posx, posy, length, height=1, rows=1):
	#self.owner = gui
	#MessagePanel.__init__(self, player, posx, posy, length, height, rows)
	#self.msg = ""
	


class MessagePanel:
    
    def __init__(self, player, posX, posY, length, height, rows=7):
        self.msgs = []
        self.posX = posX
        self.posY = posY
        self.length = length
        self.height = height
        self.rows = rows
	self.player = player
        self.panel = libtcod.console_new(length, height)
        
    def message(self, message, color=libtcod.white):
	
	
	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(message, self.length)
     
	for line in new_msg_lines:
	    #if the buffer is full, remove the first line to make room for the new one
	    if len(self.msgs) == self.rows:
		del self.msgs[0]
     
	    #add the new line as a tuple, with the text and the color
	    self.msgs.append( (line, color) )
       
                
    def update(self):
        panel = self.panel
	game_msgs = self.msgs
        
	#prepare to render the GUI panel
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)
     
	#print the game messages, one line at a time
	y = 1
	for (line, color) in game_msgs:
	    libtcod.console_set_default_foreground(panel, color)
	    libtcod.console_print_ex(panel, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
	    y += 1
	    
	#blit the contents of "panel" to the root console
	libtcod.console_blit(panel, 0, 0, self.length, self.height, 0, self.posX, self.posY)  	

class FpsCounter(MessagePanel):
    
    def __init__(self, player, posX, posY, length, height, rows=2):
	MessagePanel.__init__(self, player, posX, posY, length, height, rows)
	
    def setFps(self, fps):
	self.message(str(fps) + " FPS", libtcod.yellow)

class MousePanel(MessagePanel):
    
    def __init__(self, player, posX, posY, length, height, rows=1):
	MessagePanel.__init__(self, player, posX, posY, length, height, rows)
	self.player = player
	self.lastline = ""
	
    def refresh(self, objects, mouse):
	self.get_names_under_mouse(objects, mouse)
	
    def get_names_under_mouse(self, objects, mouse):
	m = mouse
	c = self.player.camera
	
	(x, y) = (m.cx + c.x, m.cy + c.y)
	
	#create a list with the names of all objects at the mouse's coordinates and in FOV
	names = [obj.name for obj in objects
            if obj.x == x and obj.y == y and libtcod.map_is_in_fov(c.fov_map, obj.x, obj.y)]
	line = "     "
	for name in names:
	    line += name + ", "
	line = line[0: len(line)-2].strip()
	
	if self.lastline == line:
	   return
	
	self.lastline = line
	if line == "":
	    line = "-"
	self.message(line, libtcod.yellow)
	
	

class InventoryPanel(MessagePanel):
    
    def __init__(self, player, posX, posY, length, height, rows=39):
	MessagePanel.__init__(self, player, posX, posY, length, height, rows)
	self.refresh()
	
    def refresh(self):
	player = self.player
	self.message("==========")
	self.message("INVENTORY")
	self.message("==========")
	for item in player.inventory:
	    self.message(item)
	    
class EquipmentPanel(MessagePanel):
    
    def __init__(self, player, posX, posY, length, height, rows=39):
	MessagePanel.__init__(self, player, posX, posY, length, height, rows)
	self.refresh()
	
    def refresh(self):
	player = self.player
	self.message("==========")
	self.message("EQUIPMENT")
	self.message("==========")
	#Weapons
	if player.mainHand == None:
	    self.message("Main : ")
	else:
	    self.message("Main : " + str(player.mainHand.name))
	if player.offHand == None:
	    self.message("Offhand: ")
	else:
	    self.message("Offhand : " + str(player.offHand.name))
	self.message("")
	#Armor
	if player.helmet == None:
	    self.message("Helmet : ")
	else:
	    self.message("Helmet : " + str(player.helmet.name))	    
	if player.chest == None:
	    self.message("Chest : ")
	else:
	    self.message("Chest : " + str(player.chest.name))
	if player.gloves == None:
	    self.message("Gloves : ")
	else:
	    self.message("Gloves : " + str(player.gloves.name))
	if player.legs == None:
	    self.message("Legs : ")
	else:
	    self.message("Legs : " + str(player.legs.name))
	if player.boots == None:
	    self.message("Boots : ")
	else:
	    self.message("Boots : " + str(player.boots.name))
	self.message("")
	#Accessories
	if player.necklace == None:
	    self.message("Necklace : ")
	else:
	    self.message("Necklace : " + str(player.boots.name))	
	    # Accessories
	if player.boots == None:
	    self.message("L_Ring : ")
	else:
	    self.message("L_Ring : " + str(player.ring1.name))
	if player.boots == None:
	    self.message("R_Ring : ")
	else:
	    self.message("R_Ring : " + str(player.ring2.name))

class CharacterPanel(MessagePanel):
    
    def __init__(self, player, posX, posY, length, height, rows=15):
	counter = 0
	MessagePanel.__init__(self, player, posX, posY, length, height, rows)
	self.refresh()

    def refresh(self):
	player = self.player
	Class = player.curClass
	self.message("==========")
	self.message("PLAYER")
	self.message("==========")
	self.message("Name : " + str(player.name))
	self.message("Class : " + str(Class.name))
	self.message("Level : " + str(Class.level))
	self.message("==========")
	self.message("Core Stats")
	self.message("==========")
	self.message("STR : " + str(Class.strength), libtcod.light_red)
	self.message("CON : " + str(Class.constitution), libtcod.light_orange)
	self.message("DEX : " + str(Class.dexterity), libtcod.green)
	self.message("AGI : " + str(Class.agility), libtcod.light_green)
	self.message("WIS : " + str(Class.wisdom), libtcod.light_blue)
	self.message("INT : " + str(Class.intelligence), libtcod.light_purple)

class VitalPanel:
    def __init__(self, player, posX, posY, length, height, rows=7):
        self.msgs = []
        self.posX = posX
        self.posY = posY
        self.length = length
        self.height = height
        self.rows = rows
	self.player = player
        self.panel = libtcod.console_new(length, height)
    

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color, back_color):
	panel = self.panel
	#render a bar (HP, experience, etc). first calculate the width of the bar
	bar_width = int(float(value) / maximum * total_width)
	if bar_width > total_width:
	    bar_width = total_width
     
	#render the background first
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
     
	#now render the bar on top
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
	    libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
     
	#finally, some centered text with the values
	libtcod.console_set_default_foreground(panel, libtcod.black)
	libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
            name + ': ' + str(value) + '/' + str(maximum))        
    
    def update(self):
	panel = self.panel
	player = self.player
	Class = player.curClass
	
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)
	
	lightblue = libtcod.Color(51, 153, 255)
	darkblue = libtcod.Color(74, 152, 217)	
	#show the player's stats
	
	self.render_bar(1, 1, 25, 'EXP', Class.exp, Class.tnl,
	    libtcod.yellow, libtcod.dark_grey)
	self.render_bar(1, 3, 25, 'HP', Class.hp, Class.maxHp,
	    libtcod.red, libtcod.darker_red)
	self.render_bar(1, 5, 25, 'MP', Class.mp, Class.maxMp,
	    lightblue, darkblue)
	self.render_bar(1, 7, 25, 'STA', Class.stamina, Class.maxStamina,
	    libtcod.orange, libtcod.darker_orange)

	#blit the contents of "panel" to the root console
	libtcod.console_blit(panel, 0, 0, 81, 8, 0, self.posX, self.posY)