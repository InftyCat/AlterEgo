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

from Room import *
#Info = ["Ker" , "Im"]
    
def FullOrZeroAtom (_room , fullOrZero) : #,_genus=Unc) :
    return Atom(_room,"",fullOrZero)#,_genus)

class Atom:
    def __str__ (self) :
        s = str(self.room)
        #if self.genus == Unc :
        #    s = ""
            
        return s +"_" + self.mdir + "_" + self.info
  
    def __init__(self , _room , _mdir , _info) : #, _genus = Sub) :
        if (_info in [Im, Ker,Full,Zero]) :# _mdir in [Verti,Hori,Diag] and 
            self.room = _room
            self.mdir = _mdir
            self.info = _info
        # self.genus = _genus
            self.frozen = False
        else :
            print("atom init Error!",_mdir,_info)
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
        
        #print("Coroom of" , self , " is " , (x2,y2))
        return (x2,y2)
    def isBiggerThan(self , atom):
        if self.room != atom.room :
            return False
        if self.info == Full or atom.info == Zero :
            return True
        else :
            return self.info == atom.info and self.mdir == atom.mdir 