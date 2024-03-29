#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:17:48 2024

@author: tim
"""

from Atom import Hori ,Verti, Ker, Im, Full, Zero

import Atom
class Moving :
    def __init__(self,_wld) :
        self.wld = _wld
        
    def forward (self,d) :
        s = self.wld.subobject()
        r = Atom.Atom(s.room, d,Ker).getCoRoom()
        #print("forward...",r,self.wld.areas.keys())
        if (r in self.wld.areas.keys()) :
            exact = self.wld.areas[self.wld.subobject().room].exactList()
            if ((s.info == Ker or ((d in exact) and s.info == Im)) and s.mdir == d) or s.info == Zero:
                self.wld.updateSubobject( Atom.FullOrZeroAtom(r, Zero))
            else :
                self.wld.updateSubobject(Atom.Atom(r,d,Im))
        
            
        """(x,y) = s.room
        r = (x,y+1)
        if (d == Hori) :
            r = (x+1,y)
            """
        
        
        return Atom.Atom(r,d,Im)
    def backward(self,d) :
        s = self.wld.subobject()
        room = Atom.Atom(s.room, d,Im).getCoRoom()
        exact = self.wld.areas[s.room].exactList()
        if (room in self.wld.areas.keys()) :
            
            if ((s.info == Im or (s.info == Ker and d in exact)) and s.mdir == d) :
                self.wld.updateSubobject(Atom.FullOrZeroAtom(room,Full))
            if (s.info == Zero) :
                self.wld.updateSubobject(Atom.Atom(room,d,Ker))
            
        
