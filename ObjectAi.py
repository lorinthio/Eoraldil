# -*- coding: utf-8 -*-
#import random
import math
import time
from random import randint
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod


class BasicMonster:

    def __init__(self, owner):
        self.owner = owner
        self.target = None
        self.path = None

    def takeAction(self, Map, objects):
        monster = self.owner
        if self.target == None:
            (targetfound, target) = self.checkSenses()
            if not targetfound:
                self.wander(Map, objects)
            else:           
                self.target = target
        elif 2 <= self.distance_to(self.target) <= 15:
            self.move_to_target(Map)

    def wander(self, Map, objects):
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        
        self.owner.move(dx, dy, Map, objects)
        
    def checkSenses(self):
        target = self.owner.checkSenses()
        if target is not None:
            return (True, target)
        return (False, None)

    def move_to_target(self, Map):
        #dx = x - owner.x
        #dy = y - owner.y
        #distance = math.sqrt(dx ** 2 + dy ** 2)

        #dx = int(round(dx / distance))
        #dy = int(round(dy / distance))
        #self.owner.move(dx, dy)
        
        #if path doesnt exist make new path to target
        if self.path == None:
            fov_map = Map.fov_map
            path = libtcod.path_new_using_map(fov_map)
            newx, newy = Map.randomPoint()
            libtcod.path_compute(path, self.owner.x, self.owner.y, self.target.x, self.target.y)
            # use the path ... 

            if not libtcod.path_is_empty(path) :
                x,y=libtcod.path_walk(path,True)
                if not x is None :
                    self.owner.put(x,y)
            else:
                libtcod.path_delete(self.path)
                self.path = None
            self.path = path
        #if path exists then take the next step
        else:
            path = self.path
            if not libtcod.path_is_empty(path) :
                x,y=libtcod.path_walk(path,True)
                if not x is None :
                    self.owner.put(x,y)
                else:
                    print("Empty, time for new path")
                    libtcod.path_delete(self.path)
                    self.path = None
            self.path = path

    def distance_to(self, other):
        dx = other.x - self.owner.x
        dy = other.y - self.owner.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def setTarget(self, target):
        self.target = target
