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
        # If no target then wander
        if self.owner.target == None:
            if self.owner.moveReady:
                self.wander(Map, objects)
        else:
            # If there is a target figure out the distance to determine the next action...
            distance = self.distance_to(self.owner.target)
            
            #If we can move, try to get closer (unless target is too far away)
            if self.owner.moveReady:
                self.owner.moveReady = False
                if 2 <= distance <= 10:
                    self.move_to_target(Map)
                if distance > 10: 
                    self.owner.target = None
                    
            #If we can attack, and are close enough, then attack 
            if self.owner.attackReady:    
                if distance <= 2:
                    self.owner.attack()

    def wander(self, Map, objects):
        # 40% chance to move, 60% chance to stand still
        self.owner.moveReady = False
        
        if randint(1,100) <= 40:
            dx = randint(-1, 1)
            dy = randint(-1, 1)
            
            self.owner.moved = True
            self.owner.move(dx, dy, Map, objects)
        
        
            
        
    def checkSenses(self, objects):
        target = self.owner.checkSenses(objects)
        if target != None:
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
        owner = self.owner
        target = owner.target
        fov_map = Map.fov_map
        path = libtcod.path_new_using_map(fov_map)
        libtcod.path_compute(path, owner.x, owner.y, target.x, target.y)
        
        # use the path ... 
        if not libtcod.path_is_empty(path) :
            x,y=libtcod.path_walk(path,True)
            if not x is None :
                owner.put(x,y)
                
        owner.moved = True

    def distance_to(self, other):
        dx = other.x - self.owner.x
        dy = other.y - self.owner.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def setTarget(self, target):
        self.target = target
