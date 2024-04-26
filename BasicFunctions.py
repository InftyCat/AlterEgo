#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:22:39 2024

@author: tim
"""
import random
from enum import Enum
class Helper(Enum) :
    UseUncertaintyForAssumption = 1
    EliminateToOtherMolecules = 2
   
class Genus(Enum) :
    Unc = 1
    Sub = 2
def e(x , A ) : 
    if not (isinstance(x , A)) : 
        raise Exception("Type checking fails" , x , A)    
def index_of (lst , x) :
    l = get_indices(lst,x)
    if (len(l) == 0) :
        return -1
    else :
        return l[0]
def get_indices(lst, *x):
    return [i for i, element in enumerate(lst) if element in x]
def subList(l1,l2) :
         for i in l1 :
            if (not (i in l2)) :
                 return False
         return True 
def so(s):
    return sorted(list(s))
def get_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    #print("rnd")
    return f'#{red:02x}{green:02x}{blue:02x}'
def getWidth(x,y) :
    maxX = 4
    maxY = 1
    w = 6
    wx = (maxX - x) * w 
    wy = (maxY - y) * w 
    return wx + wy
def invert (dire) :
    
        if dire== "N" : 
            return "S"
        if dire== "S" : 
            return "N"
        if dire== "W" : 
            return "O"
        if dire== "O" : 
            return "W"
        return ''.join(map(invert,list(dire)))


def comPnts(p1,p2) :
    #print(p1,p2)
    (x1,y1) = p1
    (x2,y2) = p2
    return (abs(x1 - x2) < 20 and (abs(y1-y2) < 20))
def inList(self,others,eq) :
        for o in others:
            if (eq (self , o)) : return True
        return False
                  