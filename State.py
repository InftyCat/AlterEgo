#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:59:54 2024

@author: tim
"""
import Atom
def newState(_wld,_subobject,uncRoom)  :
        return State(_wld,_subobject , _wld.genUnc(_subobject.room, uncRoom))
def genFullUnc (subobject) :
     return Atom.FullOrZeroAtom(subobject , Atom.Full)
class State :
    def __str__(self) :
        return "(" + str(self.subobject) + "," + str(self.uncertainty) + ")"
    def __init__ (self,_wld,_subobject , _uncertainty) :
        self.wld = _wld
        self.subobject = _subobject
        self.uncertainty = _uncertainty
        #print("inited" , _subobject,_uncertainty)
    def isBiggerThan(self,state) :
         
         myUnc = self.uncertainty.getKernelRoom()
         unc = state.uncertainty.getKernelRoom()
         b = myUnc.isDeeperThan(unc) 
         ret = b and self.subobject.isBiggerThan(state.subobject)
         #print(self , " > " , state , "=" , ret)
         return ret
         
