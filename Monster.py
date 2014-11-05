from random import *
from copy import *
from Object import *
<<<<<<< HEAD
from ObjectAi import *
=======
>>>>>>> origin/master

#Simply a placeholder until I work on this more


	
class MonsterHandler:
	def __init__(self):
		self.makeMonsters()

	def spawnMonster(self, areaType):
		if areaType == "Forest":
			choose(self.monsterGroups["Forest"])
		if areaType == "Cave":
			mob = choice(self.monsterGroups["Cave"])
			return mob
		
	def makeMonsters(self):
		self.monsterGroups = {}
		self.monsterGroups["Forest"] = self.makeForestCreatures()
		self.monsterGroups["Cave"] = self.makeCaveCreatures()
		#self.monsterGroups["Highlands"] = makeHighlandCreatures()
		#self.monsterGroups["Dungeon"] = makeDungeonCreatures()
		#self.monsterGroups["Elite"] = makeEliteCreatures()
		
	def makeForestCreatures(self):
		forest = []
		
		#1) Instantiate the monster with name
		#2) Set basic stats
		#3) Set its possible list of attacks [rolls, maxnumber] [3,6] will "roll" a 6 sided die 3 times
		DireRabbit = Monster("Dire Rabbit")
		DireRabbit.setStats(15, 12, 16, 16, 12, 12)
		DireRabbit.setAttacks({"Bite": [1, 6], "Feral Bite": [3,4]})
		forest.append(DireRabbit)
		
		return forest
	
	def makeCaveCreatures(self):
		cave = []
		
		Bslime = Creature("Blue Slime", size="small")
		Bslime.setStats(8, 8, 12, 16, 8, 8)
		Bslime.setAttacks({"Suck": [1,4], "Slam": [2, 3]})
		cave.append(Bslime)
		
		Gslime = Monster("Green Slime", size="small")
		Gslime.setStats(10, 9, 13, 13, 8, 8)
		Gslime.setAttacks({"Suck": [1,4], "Slam": [2, 3]})
		cave.append(Gslime)
		return cave
		
	
class Creature(EntityObject):
	def __init__(self, Name, color=libtcod.blue, size="medium"):
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
		self.size = size
		
		self.hp = 30
		self.maxHp = 30
		
		self.mp = 30
		self.maxMp = 30
		
		self.stamina = 30
		self.maxStamina = 30
		
		# Attributes
		self.strength = 10
		self.constitution = 10
		self.dexterity = 10
		self.agility = 10
		self.wisdom = 10
		self.intelligence = 10

		# Make it a map object
		EntityObject.__init__(self, 1, 1, self.name[0], color, solid=True)
		
	def setAttacks(self, attacks):
		self.attacks = attacks
		
	def setStats(self, STR, CON, DEX, AGI, WIS, INT):
		self.strength = STR
		self.constitution = CON
		self.dexterity = DEX
		self.agility = AGI
		self.wisdom = WIS
		self.intelligence = INT
		
	def updateStats(self):
		if self.size == "small":
			self.hp += (self.constitution - 12) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 12) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 12) * 3
			self.maxStamina = self.stamina
		
<<<<<<< HEAD
	def setTarget(self, target):
		self.target = target
=======
>>>>>>> origin/master
		
	def spawn(self, Map):
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
		
		spawn_mob.updateStats()
		
		(self.x, self.y) = Map.randomPoint()
		
	def attack(self, target):
		attacks = self.attacks.keys()
		NameAttack = choice(list(attacks))
		
		attack = self.attacks[NameAttack]
		damage = 0
		for i in range(attack[0]):
			damage += randint(1, attack[1])
		print(self.name + " has used " + NameAttack + " for " + str(damage) + " damage.")

	def takeAction(self, Map, MapObjects):
		self.actor.takeAction(Map, MapObjects)

class Monster(Creature):
	
	def __init__(self, Name, size="medium"):
		#Skill storage
		Creature.__init__(self, Name, libtcod.red, size)
<<<<<<< HEAD
		self.actor = BasicMonster(self)
=======
>>>>>>> origin/master
		self.aggresive = True
		
class Boss(Monster):
	
	def __init__(self, Name):
		pass
