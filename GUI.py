import textwrap
import libtcodpy as libtcod

<<<<<<< HEAD
#class CharacterPanel:

class GUIHandler:
    def __init__(self, player):
	self.gui_panels = []
	
	#Message Panels
	gui_message = MessagePanel(player, 40, 41, 40, 10)
	gui_message.message("Welcome to Eoraldil!", libtcod.yellow)
	gui_message.message("Your journey beging... in a cave. A dark, and lonely cave", libtcod.grey)
	gui_panels.append(gui_message)
	
	#Vital Panels
	gui_vitals = VitalPanel(player, 0, 41, 40, 10)
	gui_panels.append(gui_vitals)	
	
    def update(self):
	for panel in self.gui_panels:
	    panel.update()

class MessagePanel:
=======
class MessageHandler:
>>>>>>> origin/master
    
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
           
<<<<<<< HEAD
       
                
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
    
=======
>>>>>>> origin/master
    def render_bar(self, x, y, total_width, name, value, maximum, bar_color, back_color):
	panel = self.panel
	#render a bar (HP, experience, etc). first calculate the width of the bar
	bar_width = int(float(value) / maximum * total_width)
     
	#render the background first
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
     
	#now render the bar on top
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
	    libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
     
	#finally, some centered text with the values
<<<<<<< HEAD
	libtcod.console_set_default_foreground(panel, libtcod.black)
	libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
            name + ': ' + str(value) + '/' + str(maximum))        
    
    def update(self):
	panel = self.panel
	
	#show the player's stats
	player = self.player
	self.render_bar(1, 1, 25, 'EXP', player.curClass.exp, player.curClass.tnl,
	    libtcod.grey, libtcod.dark_grey)
	self.render_bar(1, 3, 25, 'HP', player.curClass.hp, player.curClass.maxHp,
	    libtcod.red, libtcod.darker_red)
	self.render_bar(1, 5, 25, 'MP', player.curClass.mp, player.curClass.maxMp,
	    libtcod.blue, libtcod.darker_blue)
	self.render_bar(1, 7, 25, 'STA', player.curClass.stamina, player.curClass.maxStamina,
	    libtcod.orange, libtcod.darker_orange)

	#blit the contents of "panel" to the root console
	libtcod.console_blit(panel, 0, 0, 81, 8, 0, self.posX, self.posY)    
=======
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
            name + ': ' + str(value) + '/' + str(maximum))           
                
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
	    libtcod.console_print_ex(panel, 40, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
	    y += 1
     
	#show the player's stats
	player = self.player
	self.render_bar(1, 1, 20, 'HP', player.curClass.hp, player.curClass.maxHp,
	    libtcod.red, libtcod.darker_red)
	self.render_bar(1, 3, 20, 'MP', player.curClass.mp, player.curClass.maxMp,
	    libtcod.blue, libtcod.darker_blue)
	self.render_bar(1, 5, 20, 'STA', player.curClass.stamina, player.curClass.maxStamina,
	    libtcod.orange, libtcod.darker_orange)
     
     
	#blit the contents of "panel" to the root console
        libtcod.console_blit(panel, 0, 0, 81, 8, 0, self.posX, self.posY)
>>>>>>> origin/master
