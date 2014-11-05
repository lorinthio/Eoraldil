# -*- coding: utf-8 -*-
#import random
import math
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod


class BasicMonster:

    def __init__(self, owner):
        self.owner = owner

    def takeAction(self, Map, MapO):
        monster = self.owner
        target = monster.target
        distance = self.distance_to(target)
        if distance >= 20:
            return       
        if distance >= 2:
            self.move_to_target(target.x, target.y, Map, MapO)

    def move_to_target(self, x, y, Map, MapO):
        owner = self.owner
        
        dx = x - owner.x
        dy = y - owner.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        owner.move(dx, dy, Map, MapO)

    def distance_to(self, other):
        owner = self.owner
        dx = other.x - owner.x
        dy = other.y - owner.y
        return math.sqrt(dx ** 2 + dy ** 2)
