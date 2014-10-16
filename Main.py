from random import *
from Character import *
from Item import *


def main():
	inp = "w"
	if inp == "w":
		player = Warrior()
	elif inp == "c":
		player = Cleric()
	elif inp == "m":
		player = Mage()
			
	IH = createItems()
	
	item = IH.genItem()
	
	player.equip(item)


def isType(obj, name):
	if name == type(obj).__name__:
		return True
	else:
		return False
	
main()