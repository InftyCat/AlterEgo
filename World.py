#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:11:14 2024

@author: tim
"""
from Particle import *
import tkinter as tkr
import random
import Segment
import Area
import BasicFunctions as Bsc
import Morphism
from Eliminator import *
from State import *
from Atom import Ker , Im ,  Full , Hori , Verti , Diag
import Atom
from Molecule import *

from Room import *
originX = 200
originY = 100
stdWidth = 300
stdHeight = 300
def dirToMdir(d) :
        ds = ["S","O","SO"]
        mdir = [Verti,Hori,Diag]
        i = Bsc.index_of(ds,d)
        if ( i >= 0): 
            return mdir[i]
        else :
            return ""

def getSubList(istart,iend,ay) :
    segs2 = ay[istart:iend+1] # ay.findAllSegments(Bsc.invert(d))
    if (iend <= istart) :
        segs2 = ay[istart:-1] + [ay[-1]] + ay[0:iend]
    return segs2

class World :
    def __init__ (self,_canvas,_subobject,goalAtom) :
        self.canvas = _canvas
        self.areas = {} #{} #[[]]
        self.morphs = {}
        
        
        state = self.canState(_subobject)
        goalstate = self.canState(goalAtom)
        elim =  elimFromGoalState(goalstate)
        self.molecules = [self.canMolecule(state,elim)]
        self.assCnt = 0
        self.implications = []                
    def applyAss(self) :
        s = self.mm().subobject().atom
        bs = []
        print("checking asses")
        for i in self.implications : 
            print(i)
            (a,b) = i
            
            if a.isBiggerThan(s) :

                # one should be able to get to original state back
                bs.append(b)
        if (self.assCnt < len(bs)) :
            
                        
            self.mm().updateStateFromSubobj(bs[self.assCnt])
            self.assCnt += 1
        else :
            self.assCnt = 0
    def morPropToImp(self) :
        epis = [ value for key, value in self.morphs.items() if value.prop== Morphism.Epi]
        monos = [value for key, value in self.morphs.items() if value.prop == Morphism.Mono]
        for e in epis :
            self.implications.append((FullOrZeroAtom(e.subobject.room, Full) , e.subobject()))
        for m in monos : 
            self.implications.append(( m.subobject() , FullOrZeroAtom(m.subobject().room, Zero) ))
          
    def subobjectAtom(self) :
        return self.mm().subobject().atom
    def move(self,forward,d) :
        self.mm().move(forward,d)
    def addArea(self,x,y,exactHori=True,c=None) :
        if (c == None) :
            c = Bsc.get_random_color()
        if (not (x,y) in self.areas) :
            #print(getWidth(x, y))
            self.areas[(x,y)] = Area.Area(self.canvas,c,Bsc.getWidth(x,y),exactHori) #[(x,y)] = c #[x].append(a)
    def addMorphism(self,xs,ys,xt,yt,prop="",specialDir = ""):
        self.addArea(xs,ys)
        self.addArea(xt,yt)        
        self.morphs[(xs,ys,xt,yt)] = self.genMor((xs,ys),(xt,yt) ,  prop)
    def swapFocus(self) :
        self.mm().swapFocus()
    def finMM(self) :
        self.mm().fin()
    def genUnc(self,room, unc) :
            if room == unc :
                return FullOrZeroAtom(room, Zero) # ,Unc)
            mdir = self.getMdir(*room,*unc)
            if (mdir == "")  :
                return FullOrZeroAtom(room, Full)# ,Unc)
            else :
                return Atom.Atom(room, mdir,Ker)# ,Unc)
    def gameEnd(self) : 
        return len(self.molecules) == 0
    def mm(self) : # main molecule
        
        return self.molecules[-1]
    def getMdir(self,x1,y1,x2,y2) :
        d = self.getDir(x1,y1,x2,y2)
        b = (x1 - x2)**2 + (y1 - y2) ** 2
        if (b == 1 or b == 2) :
            return dirToMdir(d)
        else :
            return ""    
    def addAss(self, assAtom, impAtom) :
        self.implications.append((assAtom, impAtom))

    def getDir(self,x1,y1,x2,y2) :
        d = ""
        if x1 == x2 :
            d = "S"
        elif y1 == y2 :
            d = "O"
        elif (x2 == x1 + 1 and y2 == y1 + 1) :
            d = "SO"
        if (d == "") :
            if ((x1,y1,x2,y2) in self.morphs) :
                d = self.morphs[(x1,y1,x2,y2)].specialDir
        return d        
    def out(self , x, y,allowdiag=True) :
        return [value.trg() for key, value in self.morphs.items() if value.src() == (x,y) and (allowdiag or self.getDir(*value.src() , *value.trg()) != "SO") ]
        
        
    def into(self , x, y,allowdiag=True) :
        return [value.src() for key, value in self.morphs.items() if value.trg() == (x,y)  and (allowdiag or self.getDir(*value.src() , *value.trg()) != "SO") ]
    
    
        
    def createImg(self,x2,y2,x1,y1,unc=False):
        ax = self.areas[(x1,y1)]
        ay =self.areas[(x2,y2)]
        d = self.getDir(x1,y1,x2,y2)
        #print(x1,y1,x2,y2,d)
        segs = ax.findAllSegments(d)
        
        sidx = 0
        tidx = len(segs) - 1
        #print(segs)
        while (not (Bsc.inList(segs[sidx].src() , ay.getPoints() , Bsc.comPnts))) :
            sidx +=1
        while (not (Bsc.inList(segs[tidx].trg() , ay.getPoints() , Bsc.comPnts))) :
            tidx -=1
        segs = segs[sidx:tidx+1] #list(filter(lambda s : Bsc.inList(s.src() , ay.getPoints() , Bsc.comPnts) ,  ))
        xstart = (segs[0].x1,segs[0].y1)
        xend = (segs[-1].x2,segs[-1].y2)
        #print("xstart/end",xstart,xend)
        #self.canvas.create_circle_arc(*xstart,20,start = 0,end = 359,fill="black")
        #self.canvas.create_circle_arc(*xend,30,start = 0,end = 359,fill="white")
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
            iend =iend[0] + 1
            #print(istart,iend)
            segs2 = getSubList(istart,iend,ay.segments)
            
            img= Area.Area(self.canvas,ay.c,ay.w*2) #1.5)
            for s in segs + segs2 :
                img.stealSegment(s)
                    
            return img        
    def createker(self,x1,y1,x2,y2,unc = False):
        if (x1,y1) == (x2,y2) :
           a = self.areas[(x1,y1)]
           zero = Area.Area(self.canvas,"black", a.w * 0.1 )
           for s in a.segments :
               zero.stealSegment(s)
           return zero
        else :
            return self.areas[(x1,y1)].comp(self.createImg(x2,y2,x1,y1),unc=unc)
    def jumpback(self) :
        self.mm().jumpback()
    def canMolecule2 (self, SP ,  uncAtom , _eliminator) :
        _goalState = _eliminator.targetState
        #print("creating can Molecule")
        
        UP =  lambda mol: Particle.Particle(mol,uncAtom,Genus.Unc,_goalState)
        focus = Genus.Sub
        return Molecule(self,_eliminator,SP , UP)
    def canMolecule ( self,_state ,_eliminator) :
        #self.state = State()
        #self.wld = _wld
        _goalState = _eliminator.targetState
        #self.eliminator = _eliminator
        print("creating can Molecule from state" , _state)
        SP = lambda mol : Particle.Particle(mol,_state.subobject,Genus.Sub,_goalState)
       
        focus = Genus.Sub
        return self.canMolecule2(SP , _state.uncertainty , _eliminator) #Molecule(self,_eliminator,SP , UP)
        
    def subobject(self) :
        return self.mm().subobject()
    def canState (self,_subobject) :
            return newState(self,_subobject,_subobject.room)   
    

    
    def drawAreas(self) :
        for coords in self.areas.keys() :        
            self.areas[coords].drawSegments()
    def genMor(self,s,t,p) :
        return Morphism.Morphism(*s,*t,p,self.getMdir(*s , *t))
    def initialize(self) : 
        dr = []
        ul = []
        dl = []
        ur = []
        for coords in self.areas.keys() :
            o = self.out(*coords,allowdiag=False)
            i = self.into(*coords,allowdiag=False)
            curveDR = False
            curveUL = False
            #print(coords,o,i)
            if len(o) >= 2 :
                t = Bsc.maximum(o)
                
                curveDR = not (any(map(lambda s : self.genMor(s,t,Morphism.Epi).inList(self.morphs.values()) , o)))
                
            if len(i) >= 2 :
                s = Bsc.minimum(i)
                #print("lol",s)
                curveUL = not (any(map(lambda t : self.genMor(s,t,Morphism.Mono).inList(self.morphs.values()), i)))
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
            if (x-1,y) in self.areas.keys() :

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
        self.mm().initState() 
        self.morPropToImp()