#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:11:14 2024

@author: tim
"""

import tkinter as tkr
import random
import Segment
import Area
import BasicFunctions as Bsc
import Morphism
import Moving
from Atom import Ker , Im , getDir , Full
import Atom
import Moving
originX = 200
originY = 100
stdWidth = 300
stdHeight = 300

def getSubList(istart,iend,ay) :
    segs2 = ay[istart:iend+1] # ay.findAllSegments(Bsc.invert(d))
    if (iend <= istart) :
        segs2 = ay[istart:-1] + [ay[-1]] + ay[0:iend]
    return segs2
class World :
    def __init__ (self,_canvas,_atom) :
        self.canvas = _canvas
        self.areas = {} #{} #[[]]
        self.morphs = {}
        self.atom = _atom
        self.subobject = None
        self.assCnt = 0
        self.mvg = Moving.Moving(self)
    def addArea(self,x,y,exactHori=True,c=None) :
        if (c == None) :
            c = Bsc.get_random_color()
        if (not (x,y) in self.areas) :
            #print(getWidth(x, y))
            self.areas[(x,y)] = Area.Area(self.canvas,c,Bsc.getWidth(x,y),exactHori) #[(x,y)] = c #[x].append(a)
    def addMorphism(self,xs,ys,xt,yt,prop=""):
        self.addArea(xs,ys)
        self.addArea(xt,yt)
        
        
        
        
        self.morphs[(xs,ys,xt,yt)] = Morphism.Morphism (xs,ys,xt,yt ,  prop)
    def out(self , x, y) :
        return [value.trg() for key, value in self.morphs.items() if value.src() == (x,y)]
        
        
    def into(self , x, y) :
        return [value.src() for key, value in self.morphs.items() if value.trg() == (x,y)]
    
        
    def createImg(self,x2,y2,x1,y1):
        ax = self.areas[(x1,y1)]
        ay =self.areas[(x2,y2)]
        d = Atom.getDir(x1,y1,x2,y2)
        print(x1,y1,x2,y2)
        segs = ax.findAllSegments(d)
        
        sidx = 0
        tidx = len(segs) - 1
        
        while (not (Bsc.inList(segs[sidx].src() , ay.getPoints() , Bsc.comPnts))) :
            sidx +=1
        while (not (Bsc.inList(segs[tidx].trg() , ay.getPoints() , Bsc.comPnts))) :
            tidx -=1
        segs = segs[sidx:tidx+1] #list(filter(lambda s : Bsc.inList(s.src() , ay.getPoints() , Bsc.comPnts) ,  ))
        xstart = (segs[0].x1,segs[0].y1)
        xend = (segs[-1].x2,segs[-1].y2)
        print("xstart/end",xstart,xend)
    
        istart = list(filter (lambda  i : Bsc.comPnts(ay.segments[i].src() , xend) ,  range(len(ay.segments))))
        iend = list(filter (lambda i : Bsc.comPnts(ay.segments[i].trg() , xstart) , range(len(ay.segments))))
        if (len(istart) * len(iend) == 0) :
            print("create image error" )
        else :
            if (len(istart) != 1):
                print ("weird s",[str(ay.segments[i]) for i in istart])
            if (len(iend) != 1) :
                print ("werid end")
            istart = istart[0]
            iend =iend[0]
            print(istart,iend)
            segs2 = getSubList(istart,iend,ay.segments)
            
            img= Area.Area(self.canvas,ay.c,ay.w*1.5)
            for s in segs + segs2 :
                img.stealSegment(s)
                    
            return img        
    def createker(self,x1,y1,x2,y2):
        ax = self.areas[(x1,y1)]
        ay =self.areas[(x2,y2)]
        d = Atom.getDir(x1,y1,x2,y2)
        segs = ax.findAllSegments(Bsc.invert(d))
        segs2 = ay.findAllSegments(Bsc.invert(d))
        ker= Area.Area(self.canvas,ax.c,ax.w*1.5)
        for s in segs : #+ segs2 :
            ker.stealSegment(s)
                
        return ker  
    def applyAss(self) :
        r = self.atom.room
        morIn = [value for key, value in self.morphs.items() if value.trg() == r and value.prop== Morphism.Epi]
        morOut = [value for key, value in self.morphs.items() if value.src() == r and value.prop == Morphism.Mono]
        mor = morOut + morIn
        if (self.assCnt < len(mor)) :
            m = mor[self.assCnt]
            subobj = m.subobject()
            if self.assCnt < len(morOut) :
                print("checking monomorphism")
                if self.atom == subobj :
                    print("apply mono goal")
                    self.updateAtom(Atom.FullOrZeroAtom(self.atom.room, Atom.Zero))
            else :                
                    self.updateAtom(mor[self.assCnt].subobject())
            self.assCnt += 1
        else :
            self.assCnt = 0
            """
            if self.areas[r].exactHori :
                if self.atom.info == Ker :    
                    self.updateAtom(Atom.Atom(r,self.atom.mdir,Im))
                elif self.atom.info == Im :
                    self.updateAtom(Atom.Atom(r,self.atom.mdir,Ker))
                    """
        print("New atom:" , self.atom)
            # todo exactness
            
                
    def getSubArea(self) : 
        atom = self.atom
        (x1,y1) = atom.room
        (x2,y2) = atom.getCoRoom()
        #print(x1,y1,x2,y2)
        if atom.info == Ker :     
            return self.createker(x1,y1,x2,y2)
        elif atom.info == Im :
            return self.createImg(x1,y1,x2,y2)
        elif atom.info == Full :
            full = Area.Area(self.canvas,self.areas[(x1,y1)].c,15)
            for s in self.areas[(x1,y1)].segments : full.stealSegment(s)
            return full
        elif atom.info == Atom.Zero:
            zero = Area.Area(self.canvas,"black",3)
            for s in self.areas[(x1,y1)].segments : zero.stealSegment(s)
            return zero
    def initSubArea(self) : 
        self.subobject = self.getSubArea()
    def deleteAtom(self) : 
      self.subobject.eraseSegments()  
    def updateAtom(self,atom) :    
      self.deleteAtom()
      self.atom = atom
      print("Atom  is now" , atom)
      self.subobject = self.getSubArea()
      self.drawAtom()
    def move(self,forward, d) :
        
        if forward :
           #if 
          self.mvg.forward(d)
        else :
           self.mvg.backward(d)
        #print(self.atom)
    def drawAtom(self) : 
         self.subobject.drawSegments() 
         self.subobject.drawMiddlepoint()
    def drawAreas(self) :
        for coords in self.areas.keys() :        
            self.areas[coords].drawSegments()
    def initialize(self) : 
        dr = []
        ul = []
        dl = []
        ur = []
        for coords in self.areas.keys() :
            o = self.out(*coords)
            i = self.into(*coords)
            curveDR = False
            curveUL = False
            #print(coords,o,i)
            if len(o) >= 2 :
                t = Bsc.maximum(o)
                
                curveDR = not (any(map(lambda s : Morphism.Morphism(*s,*t,Morphism.Epi).inList(self.morphs.values()) , o)))
                
            if len(i) >= 2 :
                s = Bsc.minimum(i)
                #print("lol",s)
                curveUL = not (any(map(lambda t : Morphism.Morphism(*s,*t,Morphism.Mono).inList(self.morphs.values()), i)))
            if curveDR : 
                #print("dr")
                dr.append(coords) 
            if curveUL :
                ul.append(coords)
        for coords in dr:
            (x,y) = coords
            if ((self.areas[(x+1,y)].exactHori)) :
                dl.append((x+2,y))
            #if (not (Verti in self.areas(x,y+1))) : 
                
        for coords in ul:
            (x,y) = coords
            
            if ((self.areas[(x-1,y)].exactHori)) :
                ur.append((x-2,y))
        for coords in self.areas.keys() :
            st= []
            (x,y) = coords
            if (coords in dr) : st.append("SO")
            if (coords in dl) : st.append("SW")
            if (coords in ur) : st.append("NO")
            if (coords in ul) : st.append("NW")
            w = 6
            #print(coords,st)
            self.areas[coords].initialize(originX + x * (stdWidth / 2 ) -  w / 2 * (x +y),
                       originY + y * (stdHeight / 2) -  w / 2* (x + y),
                       stdWidth +  w  * (x +y)  ,stdHeight +  w  * (x +y),st)
           