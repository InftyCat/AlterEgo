#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:14:55 2024

@author: tim
"""
import BasicFunctions as Bsc
from Atom import Im , Ker , Atom
Epi = "Epi"
Mono = "Mono"

class Morphism :
    def __init__ (self, _xs,_ys,_xt,_yt,_prop,_mdir) :
        self.xs = _xs
        self.ys = _ys
        self.xt = _xt
        self.yt = _yt
        self.prop =_prop
        self.mdir = _mdir
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
            return Atom(self.trg() , self.mdir , Im)
        elif self.prop == Mono :
            return Atom(self.src() , self.mdir , Ker)
        else :
            return None