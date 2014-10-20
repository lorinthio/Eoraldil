# -*- coding: utf-8 -*-
#import random
import math
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod


class BasicMonster:

    def __init__(self, owner):
        self.owner = owner

    def takeAction(self, fov_map):
        monster = self.owner
        if(libtcod.map_is_in_fov(fov_map, monster.x, monster.y)):
            if monster.distance_to(self.target) >= 2:
                monster.move_to_target(self.target.x, self.target.y)
            elif player.

    def move_to_target(self, x, y):
        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def setTarget(self, target):
        self.target = target
