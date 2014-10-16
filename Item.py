from random import *
from copy import *

def createItems():
	IH = ItemHandler()

	#Weapons
	longsword = Weapon("Longsword", 1, 8, "Slash", "MainHand")
	IH.newItem("Longsword", longsword)
	morningstar = Weapon("Morningstar", 1, 8, "Blunt", "MainHand")
	IH.newItem("Morningstar", morningstar)
	rapier = Weapon("Rapier", 1, 6, "Pierce", "MainHand")
	IH.newItem("Rapier", rapier)
	battleaxe = Weapon("Battleaxe", 2, 6, "Slash", "MaindHand")
	IH.newItem("Battleaxe", battleaxe)
	
	
	#Armor
	makeClothArmor(IH)
	makeLeatherArmor(IH)
	makeChainArmor(IH)
	makePlateArmor(IH)

	return IH

class ItemHandler:
	
	def __init__(self):
		self.items = {}
		self.generator = ItemGenerator(self)
		
	def newItem(self, name, object):
		self.items[name] = object
		
	def getItem(self, name):
		return self.items[name]
	
	def genItem(self):
		return self.generator.makeItem()

class ItemGenerator:
	
	def __init__(self, itemHandler):
		self.itemHandler = itemHandler
		self.identifiers = self.makeIdentifiers()
		#print("Item Generator has been created")
		
	def makeItem(self):
		itemlist = self.itemHandler.items.keys()
		item = self.itemHandler.getItem(choice(list(itemlist)))
		
		if randint(1, 100) >= 80:
			identifier = choice(list(self.identifiers))
			newitem = copy(item)
			newitem.name = newitem.name + " of " + identifier.name 
		else:
			newitem = copy(item)
		
		return newitem
		
	def makeIdentifiers(self):
		identities = []
		acute = Identifier("Acute Sense", {"Pure Damage": 2})
		identities.append(acute)		
		leech = Identifier("Leeching", {"Lifesteal": 5})
		identities.append(leech)
		
		return identities

class Identifier:
	def __init__(self, name, options):
		self.name = name
		self.details = self.makeDetails(options)
		self.tooltip = self.makeToolTip()
	
	def makeToolTip(self):
		tooltip = self.name + "\n"
		for key in self.details.keys():
			if self.details[key] == 0:
				pass
			else:
				if key == "Lifesteal" or key == "Evasion":
					tooltip += key + ": " + str(self.details[key]) + "% \n"
				else:
					tooltip += key + ": " + str(self.details[key]) + " \n"
		tooltip = tooltip[:-2]
		return tooltip
		
	def makeDetails(self, options):
		#Damage Identifiers
		#  PureDamage, Lifesteal, Evasion, 
		damageIdents = ["Pure Damage", "Lifesteal", "Evasion"]	
		for ident in damageIdents:
			try:
				if options[ident] == None:
					pass # To throw error to set to 0
				else:
					pass # Already exists
			except KeyError:
				options[ident] = 0
		
		#Regen Identifiers
		#  healthRegen, manaRegen, staminaRegen
		regenIdents = ["Health Regeneration", "Mana Regeneration", "Stamina Regeneration"]
		for ident in regenIdents:
			try:
				if options[ident] == None:
					pass # To throw error to set to 0
				else:
					pass # Already exists
			except KeyError:
				options[ident] = 0	
		
		#Vital Identifiers
		#  health, mana, stamina
		vitalIdents = ["Health", "Mana", "Stamina"]
		for ident in vitalIdents:
			try:
				if options[ident] == None:
					pass # To throw error to set to 0
				else:
					pass # Already exists
			except KeyError:
				options[ident] = 0	
		
		#Defense Identifiers
		#  slash reduction, pierce reduction, blunt reduction
		defIdents = ["Slash Defence", "Pierce Defence", "Blunt Defence"]
		for ident in defIdents:
			try:
				if options[ident] == None:
					pass # To throw error to set to 0
				else:
					pass # Already exists
			except KeyError:
				options[ident] = 0	
		
		#Attribute Identifiers
		#  Strength, Constituition, Dexterity, Agility, Wisdom, Intelligence
		attriIdents = ["Strength", "Constitution", "Dexterity", "Agility", "Wisdom", "Intelligence"]
		for ident in attriIdents:
			try:
				if options[ident] == None:
					pass # To throw error to set to 0
				else:
					pass # Already exists
			except KeyError:
				options[ident] = 0
		return options

class Equipment:
	
	def __init__(self):
		self.classRequirement = []
	
	def addClassRequirement(self, className):
		self.classRequirement.append(className)
		
	def removeClassRequirement(self, className):
		self.classRequirement.remove(className)
		
	def checkClass(self, className):
		if className in self.classRequirement or len(self.classRequirement) == 0:
			return True
		else:
			return False
		
class Weapon(Equipment):
	
	def __init__(self, name, rolls, max, dType, slot=None):
		Equipment.__init__(self)
		self.name = name
		self.rolls = rolls
		self.hD = max
		self.dType = dType
		self.slot = slot
		
	def attack(self):
		damage = 0
		for i in range(self.rolls):
			damage += randint(1, self.hD)
		print(self.name + " dealt " + str(damage) + " damage")
		return damage
	
class Armor(Equipment):
	
	def __init__(self, name, armor, armorType, slot=None):
		Equipment.__init__(self)
		self.name = name
		self.armor = armor
		self.armorType = armorType
		self.slot = slot
		
		#Damage modifiers
		if armorType == "Cloth":
			self.slashMod = 1.0
			self.pierceMod = 1.0
			self.bluntMod = 1.0
		elif armorType == "Leather":
			self.slashMod = 0.9
			self.pierceMod = 1.0
			self.bluntMod = 0.8
		elif armorType == "Chain":
			self.slashMod = 0.7
			self.pierceMod = 0.9
			self.bluntMod = 0.8
		elif armorType == "Plate":
			self.slashMod = 0.8
			self.pierceMod = 0.7
			self.bluntMod = 0.9


def makeClothArmor(ItemHandler):
	IH = ItemHandler
	
	cloth_helmet = Armor("Cloth Helmet", 1, "Cloth", "Helmet")
	cloth_chest = Armor("Cloth Robes", 2, "Cloth", "Chest")
	cloth_gloves = Armor("Cloth Gloves", 1, "Cloth", "Gloves")
	cloth_leggings = Armor("Cloth Leggings", 2, "Cloth", "Legs")
	cloth_boots = Armor("Cloth Boots", 1, "Cloth", "Boots")
	IH.newItem("Cloth Helmet", cloth_helmet)
	IH.newItem("Cloth Robes", cloth_chest)
	IH.newItem("Cloth Gloves", cloth_gloves)
	IH.newItem("Cloth Leggings", cloth_leggings)
	IH.newItem("Cloth Boots", cloth_boots)
	
def makeLeatherArmor(ItemHandler):
	IH = ItemHandler
	
	leather_helmet = Armor("Leather Helmet", 1, "Leather", "Helmet")
	leather_chest = Armor("Leather Jerkin", 3, "Leather", "Chest")
	leather_gloves = Armor("Leather Gloves", 1, "Leather", "Gloves")
	leather_leggings = Armor("Leather Leggings", 3, "Leather", "Legs")
	leather_boots = Armor("Leather Boots", 2, "Leather", "Boots")	
	IH.newItem("Leather Helmet", leather_helmet)
	IH.newItem("Leather Jerkin", leather_chest)
	IH.newItem("Leather Gloves", leather_gloves)
	IH.newItem("Leather Leggings", leather_leggings)
	IH.newItem("Leather Boots", leather_boots)	
	
def makeChainArmor(ItemHandler):
	IH = ItemHandler
	
	chain_helmet = Armor("Chainmail Helmet", 2, "Chain", "Helmet")
	chain_chest = Armor("Chainmail Jerkin", 4, "Chain", "Chest")
	chain_gloves = Armor("Chainmail Gloves", 2, "Chain", "Gloves")
	chain_leggings = Armor("Chainmail Leggings", 3, "Chain", "Legs")
	chain_boots = Armor("Chainmail Boots", 2, "Chain", "Boots")
	IH.newItem("Chainmail Helmet", chain_helmet)
	IH.newItem("Chainmail Jerkin", chain_chest)
	IH.newItem("Chainmail Gloves", chain_gloves)
	IH.newItem("Chainmail Leggings", chain_leggings)
	IH.newItem("Chainmail Boots", chain_boots)	
	
	
def makePlateArmor(ItemHandler):
	IH = ItemHandler
	
	plate_helmet = Armor("Copper Plate Helmet", 3, "Plate", "Helmet")
	plate_chest = Armor("Copper Chestplate", 5, "Plate", "Chest")
	plate_gloves = Armor("Copper Plate Gloves", 3, "Plate", "Gloves")
	plate_leggings = Armor("Copper Plate Leggings", 4, "Plate", "Legs")
	plate_boots = Armor("Copper Plate Boots", 3, "Plate", "Boots")		
	IH.newItem("Copper Plate Helmet", plate_helmet)
	IH.newItem("Copper Chestplate", plate_chest)
	IH.newItem("Copper Plate Gloves", plate_gloves)
	IH.newItem("Copper Plate Leggings", plate_leggings)
	IH.newItem("Copper Plate Boots", plate_boots)		