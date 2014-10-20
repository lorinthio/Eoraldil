from random import *

#Simply a placeholder until I work on this more

def makeMonsters():
	makeForestCreatures()
	#makeAquaticCreatures()
	
def makeForestCreatures():
	DireRabbit = Monster("Dire Rabbit")
	DireRabbit.setStats(15, 12, 16, 16, 12, 12)
	DireRabbit.setAttacks({"Bite": [1, 6], "Feral Bite": [3,4]})
	
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
		
