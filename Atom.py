#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:32:33 2024

@author: tim
"""
#morphDir = ["Hori","Verti","Diag"]
import BasicFunctions as Bsc
Hori = "Hori"
Verti = "Verti"
Diag = "Diag"
Ker = "Ker"
Im = "Im"
Full = "Full"
Zero = "Zero"
#Info = ["Ker" , "Im"]
def dirToMdir(d) :
    ds = ["S","O","SO"]
    mdir = [Verti,Hori,Diag]
    return mdir[Bsc.get_indices(ds,d)[0]]
def getDir(x1,y1,x2,y2) :
        if x1 == x2 :
            d = "S"
        elif y1 == y2 :
            d = "O"
        elif (x2 == x1 + 1 and y2 == y1 + 1) :
            d = "SO"
        return d
def getMdir(x1,y1,x2,y2) :
    return dirToMdir(getDir(x1,y1,x2,y2))        
def FullOrZeroAtom (_room , fullOrZero) :
    return Atom(_room,"",fullOrZero)
    
class Atom:
    def __str__ (self) :
        return str(self.room) + "_" + self.mdir + "_" + self.info
    def __init__(self , _room , _mdir , _info) :
        self.room = _room
        self.mdir = _mdir
        self.info = _info
    def __eq__(self, other):
            if isinstance(other, Atom):
                return self.__dict__ == other.__dict__
            return False    
    def getCoRoom(self) : 
        (x1,y1) = self.room
        x2 = x1
        y2 = y1
        
        if self.info == Ker :
            vorz = 1
        if self.info == Im :
            vorz = -1
        if self.mdir == Hori :
            x2 += vorz
        if (self.mdir == Verti) : 
            y2 += vorz
        if (self.mdir == Diag) :
            x2 += vorz
            y2 += vorz
       # print("Coroom of" , self , " is " , (x2,y2))
        return (x2,y2)
        