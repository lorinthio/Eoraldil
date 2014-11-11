# -*- coding: utf-8 -*-
#import random
import math
from random import randint
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod


class BasicMonster:

    def __init__(self, owner):
        self.owner = owner
        self.target = None

    def takeAction(self, Map, objects):
        monster = self.owner
        if self.target == None:
            self.wander(Map, objects)
            return
        if 2 <= self.distance_to(self.target) <= 15:
            monster.move_to_target(self.target.x, self.target.y)

    def wander(self, Map, objects):
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        self.owner.move(dx, dy, Map, objects)

    def move_to_target(self, x, y):
        dx = x - owner.x
        dy = y - owner.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.owner.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.owner.x
        dy = other.y - self.owner.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def setTarget(self, target):
        self.target = target
