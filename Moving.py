#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:17:48 2024

@author: tim
"""

from Atom import Hori ,Verti, Ker, Im, Full, Zero
## MOVING JUST FOR SUBObJCECT Particles
import Atom
class Moving :
    def __init__(self,_wld,_molecule):
        self.molecule = _molecule
        self.wld = _wld
    """def updateIfUnc(self,room) : 
        r = self.molecule.getUncCoRoom()
        r.wedge(room)

        print(r)
   """

     #updateSubobject
        #print("finding max" , self.uncertainty().getCoRoom() , subobject.room)

    def forward (self,d) :
        #if self.molecule.genus == Unc :

        
        #print("uncRoom",uncRoom)
        s : Atom= self.molecule.atom #self.wld.subobjectAtom()
        r = Atom.Atom(s.room, d,Ker).getCoRoom()
        uncRoom  = r
        
        
        #print("forward...",r,self.wld.areas.keys())
        if (s.room+r in self.wld.morphs.keys()) :
            
            if (s.isKernel(self.wld,d)):
                self.molecule.updateAtom(Atom.FullOrZeroAtom(r, Zero)) #updateSubobject(
                
            else :
                self.molecule.updateAtom(Atom.Atom(r,d,Im))
            return True 
        #return Atom.Atom(r,d,Im)
        return False   
        """(x,y) = s.room
        r = (x,y+1)
        if (d == Hori) :
            r = (x+1,y)
            """
        
        
            
    def backward(self,d) :
        s = self.wld.subobjectAtom()
        room = Atom.Atom(s.room, d,Im).getCoRoom()
        exact = self.wld.areas[s.room].exactList()
        #print(room,s.room,self.wld.morphs.keys())
        if (room + s.room in self.wld.morphs.keys()) : #room in self.wld.areas.keys() and 
            
            if ((s.info == Im or (s.info == Ker and d in exact)) and s.mdir == d) :
                self.molecule.updateAtom(Atom.FullOrZeroAtom(room,Full))
            elif (s.info == Zero) :
                self.molecule.updateAtom(Atom.Atom(room,d,Ker))
            else :
                return False
            return True
        return False
        
