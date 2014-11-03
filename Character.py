from Item import *
from Object import *
import libtcodpy as libtcod

#When saving character data, this will need a mix of database and Pickle, so we
#   can save/load objects directly. As the modified items will be hard to store
#   otherwise... So pickle the inventories/Equipment per player, but store stats/talents in
#   database is my idea


# Generic player class, not implemented yet. Eventually will store connection data also for Multiplayer
class Player(EntityObject):
	
	def __init__(self, name):
		#Position object
		EntityObject.__init__(self, 1, 1, '@', libtcod.green, solid=True)
		
		#Equipment
		self.mainHand = None
		self.offHand = None
		
		self.helmet = None
		self.chest = None
		self.gloves = None
		self.legs = None
		self.boots = None
		
		# Accessories
		self.necklace = None
		self.ring1 = None
		self.ring2 = None
		
		# Identifiers	
		self.name = name
		self.nickName = name
		self.curClass = None
		
		
	def createPlayer(self):
		self.classes = {"Warrior": Warrior(), "Rogue": Rogue(), "Cleric": Cleric(), "Mage": Mage()}

	def loadPlayer(self):
		#Fill in for when I write up the database load and server data sending
		pass
		
	def equipClass(self, className):
		# Saves the characters current class in its storage then loads the 
		#      desired class to curClass
		try:
			self.classes[self.curClass.name] = self.curClass
			self.curClass = self.classes[className]
		except AttributeError:
			self.curClass = self.classes[className]
		
		
	def equip(self, item):
		slot = item.slot
		equippable = False
		
		Class = self.curClass
		
		# Check if it is a weapon or armor, then check if the character class
		#    can equip it (equippable = True)
		if type(item) is Weapon:
			if item.weaponType in Class.weaponTypes:
				equippable = True
			if not equippable:
				print("You cannot equip this type of weapon,", item.weaponType)
				return
		elif type(item) is Armor:
			if item.armorType in Class.armorTypes:
				equippable = True
			if not equippable:
				print("You cannot equip this type of armor,", item.armorType)			
				return
		
		#Checking which slot the item goes into then equips it there     
		if slot == "MainHand":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " in your Main Hand")
				self.mainHand = item
		elif slot == "OffHand":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " in your Off-hand")
				self.offHand = item
		elif slot == "Helmet":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " on your Head")
				self.helmet = item
		elif slot == "Chest":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " on your Chest")
				self.chest = item
		elif slot == "Gloves":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " on your Hands")
				self.gloves = item
		elif slot == "Legs":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " on your Legs")
				self.legs = item
		elif slot == "Boots":
			if item.checkClass(Class.name):
				print("You have equipped a(n) " + item.name + " on your Feet")
				self.boots = item
			
	#Simply called to put an item in the players inventory	
	def giveItem(self, item):
		size = len(self.inventory)
		if size+1 > 30:
			print("You cannot pick up the " + item.name)
		elif size+1 <= 30:
			self.inventory.append(item)
			
	#Gives exp to the player
	def giveExp(self, exp):
		
		#Gets current class equipped and gives it exp
		Class = self.curClass
		while Class.tnl <= 0:
			nextLevel = 800 + (Class.level * 200)
			Class.tnl += nextLevel
			Class.level += 1
			if Class.level % 3 == 0:
				Class.attributePoints += 1
			elif Class.level % 2 == 0:
				Class.skillPoints += 1	

class CharacterClass:
	
	def __init__(self):
		# Skills
		self.talentPoints = 1
		self.attributePoints = 5
		
		# Level / Exp
		self.experience = 0
		self.tnl = 1000
		self.level = 1
	
	def setStats(self, STR, CON, DEX, AGI, WIS, INT):
		self.strength = STR
		self.constitution = CON
		self.dexterity = DEX
		self.agility = AGI
		self.wisdom = WIS
		self.intelligence = INT		
	
class Warrior(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Bash": getattr(self, "bash")}
		self.weaponTypes = ["Normal", "Martial"]
		self.armorTypes = ["Leather", "Chain", "Plate"]
		self.name = "Warrior"
		
		# TalentTree (For skill building/customization)
		# self.talentTree = {"Bash": 1}
		
		# Vitals
		self.hp = 130
		self.maxHp = 130
		
		self.mp = 70
		self.maxMp = 70
		
		self.stamina = 100
		self.maxStamina = 100
		
		self.hpRegen = 5
		self.mpRegen = 2
		self.staRegen = 8
		
		# Attributes
		self.strength = 16
		self.constitution = 16
		self.dexterity = 15
		self.agility = 14
		self.wisdom = 12
		self.intelligence = 12		
	
	def updateStats(self):
		self.maxHp = 130 + ((self.constitution - 15) * 8)
		self.maxMp = 70 + ((self.wisdom - 10) * 4)
		self.maxStamina = 100 + ((self.strength - 15) * 5)
		
		self.hpRegen = 5 + (self.constitution / 3)
		self.mpRegen = 2 + (self.wisdom / 3)
		self.staRegen = 8 + (self.strength / 3)	
	
	def bash(self):
		print("You used bash dealing, " + str((self.stength / 2) + randint(1,8)) + " damage")
		
		
class Rogue(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Stab": getattr(self, "stab")}
		self.weaponTypes = ["Normal", "Martial", "Exotic"]
		self.armorTypes = ["Leather", "Chain"]
		self.name = "Rogue"
		
		# TalentTree (For skill building/customization)
		# self.talentTree = {"Stab": 1}		
		
		# Vitals
		self.hp = 100
		self.maxHp = 100
		
		self.mp = 70
		self.maxMp = 70
		
		self.stamina = 130
		self.maxStamina = 130
		
		# Attributes
		self.strength = 15
		self.constitution = 14
		self.dexterity = 16
		self.agility = 16
		self.wisdom = 12
		self.intelligence = 12		
	
	def updateStats(self):
		self.maxHp = 100 + ((self.constitution - 15) * 8)
		self.maxMp = 70 + ((self.wisdom - 10) * 4)
		self.maxStamina = 130 + ((self.strength - 15) * 5)
		
		self.hpRegen = 3 + (self.constitution / 3)
		self.mpRegen = 3 + (self.wisdom / 3)
		self.staRegen = 9 + (self.strength / 3)	
	
	def stab(self):
		print("You used bash dealing, " + str((self.stength / 2) + randint(1,8)) + " damage")	
		
		
class Cleric(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Heal": getattr(self, "heal")}
		self.weaponTypes = ["Normal", "Staves"]
		self.armorTypes = ["Cloth", "Leather", "Chain"]
		self.name = "Cleric"
		
		# Vitals
		self.hp = 100
		self.maxHp = 100
		
		self.mp = 100
		self.maxMp = 100
		
		self.stamina = 100
		self.maxStamina = 100
		
		# Attributes
		self.strength = 14
		self.constitution = 16
		self.dexterity = 15
		self.agility = 12
		self.wisdom = 16
		self.intelligence = 12		
	
	def updateStats(self):
		self.maxHp = 100 + ((self.constitution - 15) * 8)
		self.maxMp = 100 + ((self.wisdom - 10) * 4)
		self.maxStamina = 100 + ((self.strength - 15) * 5)
		
		self.hpRegen = 4 + (self.constitution / 3)
		self.mpRegen = 4 + (self.wisdom / 3)
		self.staRegen = 7 + (self.strength / 3)	
	
	def morningstar(self):
		print("You used a Morningstar dealing, " + str(randint(1,8)) + " damage")
		
	def heal(self):
		print("You used Heal! Restoring " + str(randint(2,8) + randint(2,8)) + " health!")


class Mage(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Fireball": getattr(self, "fireball"), "Icebolt": getattr(self, "icebolt")}
		self.weaponTypes = ["Normal", "Staves"]
		self.armorTypes = ["Cloth", "Leather"]
		self.name = "Mage"
		
		# Vitals
		self.hp = 70
		self.maxHp = 70
		
		self.mp = 150
		self.maxMp = 150
		
		self.stamina = 80
		self.maxStamina = 80
		
		# Attributes
		self.strength = 12
		self.constitution = 14
		self.dexterity = 12
		self.agility = 15
		self.wisdom = 16
		self.intelligence = 16	
	
	def updateStats(self):
		self.maxHp = 70 + ((self.constitution - 15) * 8)
		self.maxMp = 150 + ((self.wisdom - 10) * 4)
		self.maxStamina = 80 + ((self.strength - 15) * 5)
		
		self.hpRegen = 2 + (self.constitution / 3)
		self.mpRegen = 5 + (self.wisdom / 3)
		self.staRegen = 8 + (self.strength / 3)	
	
	def fireball(self):
		print("You used a Fireball dealing, " + str(randint(2,8)) + " damage")
		
	def icebolt(self):
		print("You used a Icebolt dealing, " + str(randint(1,6)) + " damage")
