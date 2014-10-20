from random import *
from Character import *
from Item import *
from Monster import *
import libtcodpy as libt


def main():
	player = Player("Lorinthio")
	player.createPlayer()
	player.equipClass("Warrior")
	
	makeMonsters()
	
	SCREEN_W = 80
	SCREEN_H = 50
	LIMIT_FPS = 30
	
	libt.console_set_custom_font('arial10x10.png', libt.FONT_TYPE_GREYSCALE | libt.FONT_LAYOUT_TCOD)
	libt.console_init_root(SCREEN_W, SCREEN_H, 'Eoraldil', False)
	libt.sys_set_fps(LIMIT_FPS)
	libt.console_set_default_foreground(0, libt.white)

	playerx = SCREEN_W/2
	playery = SCREEN_H/2	
	
	while not libt.console_is_window_closed():
		    libt.console_set_default_foreground(0, libt.white)
		    libt.console_put_char(0, playerx, playery, '@', libt.BKGND_NONE)
		 
		    libt.console_flush()
		 
		    libt.console_put_char(0, playerx, playery, ' ', libt.BKGND_NONE)
		 
		    #handle keys and exit game if needed
		    exit = handle_keys()
		    if exit:
			break


def handle_keys():
	#movement keys
	key = libt.console_check_for_keypress(libt.KEY_PRESSED)
	if key.vk == libt.KEY_CHAR:
		if key.c == ord('w'):
		    playery -= 1
		    print('w')
		elif key.c == ord('s'):
		    playery += 1
		    print('s')
		elif key.c == ord('a'):
		    playerx -= 1
		    print('a')
		elif key.c == ord('d'):
		    playerx += 1
		    print('d')
	if key.vk == libt.KEY_ENTER and key.lalt:
	    #Alt+Enter: toggle fullscreen
	    libt.console_set_fullscreen(not libt.console_is_fullscreen())
     
	elif key.vk == libt.KEY_ESCAPE:
	    return True  #exit game		


def dropItem():
	IH = createItems()
	
	item = IH.genItem()
	
	player.equip(item)


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
