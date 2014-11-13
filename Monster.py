from random import *
from copy import *
from Object import *
from ObjectAi import *

#Simply a placeholder until I work on this more


	
class MonsterHandler:
	def __init__(self):
		self.makeMonsters()

	def spawnMonster(self, Map):
                areaType = Map.mapType
		if "forest" in areaType.lower():
			mob = choice(self.monsterGroups["Forest"])
		elif "cave" in areaType.lower():
			mob = choice(self.monsterGroups["Cave"])
		elif "dungeon" in areaType.lower():
                        mob = choice(self.monsterGroups["Dungeon"])
		return mob.spawn(Map)
		
	def makeMonsters(self):
		self.monsterGroups = {}
		self.monsterGroups["Forest"] = self.makeForestCreatures()
		self.monsterGroups["Cave"] = self.makeCaveCreatures()
		#self.monsterGroups["Highlands"] = makeHighlandCreatures()
		self.monsterGroups["Dungeon"] = self.makeDungeonCreatures()
		#self.monsterGroups["Elite"] = makeEliteCreatures()

        def makeDungeonCreatures(self):
                dungeon = []
                
                smallOrc = Monster("Young Orc", size="small")
                smallOrc.setStats(16, 14, 11, 10, 8, 8)
                smallOrc.setAttacks({"Slash": [1, 6], "Chop": [2, 4]})
                dungeon.append(smallOrc)
		
		return dungeon
                
		
	def makeForestCreatures(self):
		forest = []
		
		#1) Instantiate the monster with name
		#2) Set basic stats
		#3) Set its possible list of attacks [rolls, maxnumber] [3,6] will "roll" a 6 sided die 3 times
		DireRabbit = Monster("Dire Rabbit", size="small")
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
		
		bat = Creature("Bat", size ="tiny")
		bat.setStats(7, 6, 14, 14, 8, 8)
		bat.setAttacks({"Bite": [2,2]})
		cave.append(bat)
		
		return cave
		
	
class Creature(EntityObject):
	def __init__(self, Name, color=libtcod.blue, size="medium"):
		# Make it a map object
		EntityObject.__init__(self, 1, 1, Name[0], color, solid=True)		
		
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
		
		# Misc Attributes
		self.moveSpeed = 3.0
		self.moveTimer = 0
		self.attackSpeed = 2.0
		self.attackTimer = 0

		self.ai = BasicMonster(self)
		
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
		agility = self.agility
		if self.size == "tiny":
			self.hp += (self.constitution - 13) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 13) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 14) * 3
			self.maxStamina = self.stamina
			
			self.moveSpeed = ((80 - agility) / 70.00) *   1.50
		elif self.size == "small":
			self.hp += (self.constitution - 12) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 11) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 12) * 3
			self.maxStamina = self.stamina
			
			self.moveSpeed = ((80 - agility) / 66.00) *   1.75
		elif self.size == "medium":
			self.hp += (self.constitution - 10) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 8) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 10) * 3
			self.maxStamina = self.stamina
			
			self.moveSpeed = ((80 - agility) / 62.00) *   2.00
		elif self.size == "large":
			self.hp += (self.constitution - 7) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 12) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 7) * 3
			self.maxStamina = self.stamina
			
			self.moveSpeed = ((80 - agility) / 60.00) *   2.50
		elif self.size == "giant":
			self.hp += (self.constitution - 4) * 3
			self.maxHp = self.hp
			self.mp += (self.wisdom - 12) * 3
			self.maxMp = self.mp
			self.stamina = (self.strength - 4) * 3
			self.maxStamina = self.stamina
			
			self.moveSpeed = ((80 - agility) / 58.00) *   3.00	
		
	def takeAction(self, deltaT, Map, objects):
		self.moveTimer += deltaT
		moveReady = False
		attackReady = False
		
		if self.moveTimer >= self.moveSpeed:
			moveReady = True
			self.moveTimer -= self.moveSpeed
		self.attackTimer += deltaT
		if self.attackTimer >= self.attackSpeed:
			attackReady = True
			self.attackTimer -= self.attackSpeed
			
		if moveReady or attackReady:
			self.ai.takeAction(Map, objects)
			return True
		
	def spawn(self, Map=None):
		spawn_mob = deepcopy(self)
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
		spawn_mob.Map = Map
		
		(spawn_mob.x, spawn_mob.y) = Map.randomSpawnPoint(self)

		return spawn_mob
		
	def checkSenses(self):
		pass
		
	def attack(self, target):
		attacks = self.attacks.keys()
		NameAttack = choice(list(attacks))
		
		attack = self.attacks[NameAttack]
		damage = 0
		for i in range(attack[0]):
			damage += randint(1, attack[1])
		print(self.name + " has used " + NameAttack + " for " + str(damage) + " damage.")


class Monster(Creature):
	
	def __init__(self, Name, size="medium"):
		#Skill storage
		Creature.__init__(self, Name, libtcod.red, size)
		self.aggresive = True
		
class Boss(Monster):
	
	def __init__(self, Name):
		pass
