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
        s = self.wld.atom
        r = Atom.Atom(s.room, d,Ker).getCoRoom()
        print("forward...",r,self.wld.areas.keys())
        if (r in self.wld.areas.keys()) :
            exact = self.wld.areas[self.wld.atom.room].exactList()
            if ((s.info == Ker or ((d in exact) and s.info == Im)) and s.mdir == d) or s.info == Zero:
                self.wld.updateAtom( Atom.FullOrZeroAtom(r, Zero))
            else :
                self.wld.updateAtom(Atom.Atom(r,d,Im))
        
            
        """(x,y) = s.room
        r = (x,y+1)
        if (d == Hori) :
            r = (x+1,y)
            """
        
        
        return Atom.Atom(r,d,Im)
    def backward(self,d) :
        s = self.wld.atom
        room = Atom.Atom(s.room, d,Im).getCoRoom()
        exact = self.wld.areas[self.wld.atom.room].exactList()
        if (room in self.wld.areas.keys()) :
            
            if ((s.info == Im or (s.info == Ker and d in exact)) and s.mdir == d) :
                self.wld.updateAtom(Atom.FullOrZeroAtom(room,Full))
            if (s.info == Zero) :
                self.wld.updateAtom(Atom.Atom(room,d,Ker))
            
        
