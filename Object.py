# -*- coding: utf-8 -*-
from sys import path as syspath
syspath.append('.//libtcod-1.5.1')
import libtcodpy as libtcod

class UseableObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def use(self):
        print("Tried to use ", self, " but no code written")

class Door(UseableObject):

    def __init__(self, x, y, needkey=False):
        UseableObject.__init__(self, x, y)
        self.char = 'D'
        self.name = 'Door'
        self.solid = True
        self.color = libtcod.white
        self.needkey = needkey
        self.closed = True

    def use(self):
        if not needkey:
            if self.closed:
                self.char = 'd'
                self.solid = False
                self.closed = False
            else:
                self.char = 'D'
                self.solid = True
                self.closed = True
            

class EntityObject():

    def __init__(self, x, y, char="", color=libtcod.green, solid=True, localMap=None):
        self.localMap = localMap
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.solid = solid
        self.direction = "North"

    def put(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.findDirection(dx, dy)
        
        self.x = x
        self.y = y

    def findDirection(self, dx, dy):
        #To find the direction the Entity is facing
        d = ""
        if dy == -1:
            d += "North"
        elif dy == 1:
            d += "South"        
        if dx == 1:
            d += "East"
        elif dx == -1:
            d += "West"
        
        if d != "":
            self.direction = d

    def move(self, dx, dy, Map, objects):
        x = self.x + dx
        y = self.y + dy
        if not self.is_blocked(Map, x, y, objects):
            self.x = x
            self.y = y
            self.findDirection(dx, dy)

    def is_blocked(self, Map, x, y, objects):
        #first test the map tile
        if Map.mappedArea[x][y].blocked:
            return True

        #now check for any blocking objects
        for Object in objects:
            if Object.solid and Object.x == x and Object.y == y:
                return True

        return False
    
    def draw(self, console, offsetx=0, offsety=0, target=False):
        if not target:
            libtcod.console_set_default_foreground(console, self.color)
        else:
            libtcod.console_set_default_foreground(console, libtcod.yellow)
        libtcod.console_put_char(console, (self.x - offsetx), (self.y - offsety), self.char, libtcod.BKGND_NONE)

    def clear(self, console, offsetx=0, offsety=0):
        libtcod.console_put_char(console, (self.x - offsetx), (self.y - offsety), ' ', libtcod.BKGND_NONE)

    def giveStats(self, stat):
        self.stats = stat

    def setAi(self, ai):
        self.ai = ai
