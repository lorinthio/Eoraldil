from random import *
from copy import *

#Simply a placeholder until I work on this more


	
class MonsterHandler:
	def __init__(self):
		self.makeMonsters()

	def makeMonsters(self):
		self.monsterGroups = {}
		self.monsterGroups["Forest"] = makeForestCreatures()
		#self.monsterGroups["Cave"] = makeCaveCreatures()
		#self.monsterGroups["Highlands"] = makeHighlandCreatures()
		#self.monsterGroups["Dungeon"] = makeDungeonCreatures()
		#self.monsterGroups["Elite"] = makeEliteCreatures()
		
	def makeForestCreatures(self):
		forestMobs = []
		
		#1) Instantiate the monster with name
		#2) Set basic stats
		#3) Set its possible list of attacks [rolls, maxnumber] [3,6] will "roll" a 6 sided die 3 times
		DireRabbit = Monster("Dire Rabbit")
		DireRabbit.setStats(15, 12, 16, 16, 12, 12)
		DireRabbit.setAttacks({"Bite": [1, 6], "Feral Bite": [3,4]})
		forestMobs.append(DireRabbit)
		
		return forestMobs
	
class Creature:
	def __init__(self, Name):
		#Skill storage
		self.name = Name
		self.aggresive = False
		self.attacks = {}
		
		# Equipment
		self.mainHand = None
		self.offHand = None
		
		self.helmet = None
		self.chest = None
		self.gloves = None
		self.legs = None
		self.boots = None
		
		# Vitals
		self.hp = 130
		self.maxHp = 130
		
		self.mp = 70
		self.maxMp = 70
		
		self.stamina = 100
		self.maxStamina = 100
		
		# Attributes
		self.strength = 16
		self.constitution = 16
		self.dexterity = 15
		self.agility = 14
		self.wisdom = 12
		self.intelligence = 12
		
	def setAttacks(self, attacks):
		self.attacks = attacks
		
	def setStats(self, STR, CON, DEX, AGI, WIS, INT):
		self.strength = STR
		self.constitution = CON
		self.dexterity = DEX
		self.agility = AGI
		self.wisdom = WIS
		self.intelligence = INT
		
	def spawn(self):
		spawn_mob = copy(self)
		strmod = randint(-3, 3)
		conmod = randint(-3, 3)
		dexmod = randint(-3, 3)
		agimod = randint(-3, 3)
		wismod = randint(-3, 3)
		intmod = randint(-3, 3)
		
		spawn_mob.strength += strmod
		spawn_mob.constitution += conmod
		spawn_mob.dexterity += dexmod
		spawn_mob.agility += agimod
		spawn_mob.wisdom += wismod
		spawn_mob.intelligence += intmod
		
	def attack(self, target):
		attacks = self.attacks.keys()
		NameAttack = choice(list(attacks))
		
		attack = self.attacks[NameAttack]
		damage = 0
		for i in range(attack[0]):
			damage += randint(1, attack[1])
		print(self.name + " has used " + NameAttack + " for " + str(damage) + " damage.")


class Monster(Creature):
	
	def __init__(self, Name):
		#Skill storage
		self.aggresive = True
		Creature.__init__(self, Name)
		
class Boss(Monster):
	
	def __init__(self, Name):
		pass
