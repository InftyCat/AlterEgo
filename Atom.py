#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:32:33 2024

@author: tim
"""
#morphDir = ["Hori","Verti","Diag"]
import BasicFunctions as Bsc
import Area
Hori = "Hori" 
Verti = "Verti"
Diag = "Diag"
Ker = "Ker"
Coker = "Coker"
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
        #if self.genus == Genus.Unc :
        #    s = ""
        
        return s +"_" + self.showDirInf() #self.mdir + "_" + self.info
    def showDirInf(self) :
         s = self.mdir + "_"
         if self.mdir == "" :
              s = ""
         return s + self.info
    def isKernel(self , wld,d=None) :
        if d== None :
             return self.isKernel(wld , Hori) or self.isKernel(wld,Verti)
        else :
            exact = wld.areas[self.room].exactList()
            return ((self.info == Ker or ((d in exact) and self.info == Im)) and self.mdir == d) or self.info == Zero
    def __init__(self , _room , _mdir , _info) : #, _genus = Genus.Sub) :
        
        if (_info in [Im, Ker,Coker ,Full,Zero]) :# _mdir in [Verti,Hori,Diag] and 
            self.room = _room
            self.mdir = _mdir
            self.info = _info
        # self.genus = _genus
            
        else :
            print("atom init Error!",_mdir,_info)
    def getArea(self , wld) : 
           
            (x1,y1) = self.room
            
            (x2,y2) = self.getCoRoom()
            #print(".",self,(x1,y1),(x2,y2))
            #print(x1,y1,x2,y2)
            if self.info == Ker :     
                return wld.createker(x1,y1,x2,y2)
            elif self.info == Im :
                return wld.createImg(x1,y1,x2,y2)
            elif self.info == Coker : 
                return wld.createCoker(x1,y1,x2,y2)
            
            elif self.info == Full :
                full = Area.Area(wld.canvas,wld.areas[(x1,y1)].c,15)
                for s in wld.areas[(x1,y1)].segments : full.stealSegment(s)
                return full
            elif self.info == Zero:
                zero = Area.Area(wld.canvas,"#000000",3)
                for s in wld.areas[(x1,y1)].segments : zero.stealSegment(s)
                return zero
    def __eq__(self, other):
            if isinstance(other, Atom):
                return self.__dict__ == other.__dict__
            return False    
    def getKernelRoom(self,unc=True) : 
        if unc : 
            if self.info == Full :
                    return Room(None,True)
            if self.info == Zero :
                    return Room(self.room)        
        return Room(self.getCoRoom())
    def getCoRoom(self) : 
        
        (x1,y1) = self.room
        x2 = x1
        y2 = y1
        
        if self.info == Ker :
            vorz = 1
        if self.info == Im :
            vorz = -1
        if self.info == Coker : # if f : A -> B, then coker f is a room of B with coroom A.
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
        ret = False
        if (not isinstance(atom,Atom)) : 
             print("Atom comparing error")
             return
        if self.room != atom.room :
            ret = False
        else :
            if self.info == Full or atom.info == Zero :
                ret = True
            else :
                ret = self.info == atom.info and self.mdir == atom.mdir 
        #print(self, ">" , atom, "=",ret)
        return ret