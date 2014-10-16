from Item import *

class CharacterClass:
	
	def __init__(self):
		# Equipment
		self.inventory = []
		
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
		
		# Skills
		self.skillPoints = 3
		self.attributePoints = 3
		
		# Level / Exp
		self.experience = 0
		self.tnl = 1000
		self.level = 1
		
		
	def equip(self, item):
		slot = item.slot
		equippable = False
		
		# Check if it is a weapon or armor, then check if the character class
		#    can equip it (equippable = True)
		if type(item) is Weapon:
			print("item is a weapon")
		elif type(item) is Armor:
			if item.armorType in self.armorTypes:
				equippable = True

		if not equippable:
			return print("You cannot equip this type of item")
		     
		if slot == "MainHand":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " in your Main Hand")
				self.mainHand = item
		elif slot == "OffHand":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " in your Off-hand")
				self.offHand = item
		elif slot == "Helmet":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " on your Head")
				self.helmet = item
		elif slot == "Chest":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " on your Chest")
				self.chest = item
		elif slot == "Gloves":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " on your Hands")
				self.gloves = item
		elif slot == "Legs":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " on your Legs")
				self.legs = item
		elif slot == "Boots":
			if item.checkClass(self.name):
				print("You have equipped a(n) " + item.name + " on your Feet")
				self.boots = item
				
	def giveItem(self, item):
		size = len(self.inventory)
		if size+1 > 30:
			print("You cannot pick up the " + item.name)
		elif size+1 <= 30:
			self.inventory.append(item)
			
	def giveExp(self, exp):
		while self.tnl <= 0:
			nextLevel = 800 + (self.level * 200)
			self.tnl += nextLevel
			self.level += 1
			if self.level % 3 == 0:
				self.attributePoints += 1
			elif self.level % 2 == 0:
				self.skillPoints += 1
	
	
class Warrior(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Bash": getattr(self, "bash")}
		self.armorTypes = ["Leather", "Chain", "Plate"]
		self.name = "Warrior"
		
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
		self.skills = {"Bash": getattr(self, "bash")}
		self.armorTypes = ["Leather", "Chain"]
		self.name = "Rogue"
		
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
	
	def bash(self):
		print("You used bash dealing, " + str((self.stength / 2) + randint(1,8)) + " damage")	
		
		
class Cleric(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Heal": getattr(self, "heal")}
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
	
	def morningstar(self):
		print("You used a Morningstar dealing, " + str(randint(1,8)) + " damage")
		
	def heal(self):
		print("You used Heal! Restoring " + str(randint(2,8) + randint(2,8)) + " health!")


class Mage(CharacterClass):
	
	def __init__(self):
		CharacterClass.__init__(self)
		self.skills = {"Fireball": getattr(self, "fireball"), "Icebolt": getattr(self, "icebolt")}
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
	
	def fireball(self):
		print("You used a Fireball dealing, " + str(randint(2,8)) + " damage")
		
	def icebolt(self):
		print("You used a Icebolt dealing, " + str(randint(1,6)) + " damage")