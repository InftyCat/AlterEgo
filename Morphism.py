#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:14:55 2024

@author: tim
"""
import BasicFunctions as Bsc
from Atom import getMdir , Im , Ker , Atom
Epi = "Epi"
Mono = "Mono"

class Morphism :
    def __init__ (self, _xs,_ys,_xt,_yt,_prop) :
        self.xs = _xs
        self.ys = _ys
        self.xt = _xt
        self.yt = _yt
        self.prop =_prop
    def src (self) :
        return (self.xs,self.ys)
    def trg(self) :
        return (self.xt,self.yt)
    def __eq__(self, other):
        if isinstance(other, Morphism):
            return self.__dict__ == other.__dict__
        return False        
    def inList(self,others) :
       return Bsc.inList(self,others,(lambda f , g : f == g))
    def subobject(self) :
        if self.prop == Epi:
            return Atom(self.trg() , getMdir(*self.src(), *self.trg()) , Im)
        elif self.prop == Mono :
            return Atom(self.src() , getMdir(*self.src(), *self.trg()) , Ker)
        else :
            return None