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
from MovingUnc import MovingUnc

from Room import *
stdWidth = 500
stdHeight = 500
originX = 200
originY = 100

from enum import Enum

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
stdHelper = [Helper.EliminateToOtherMolecules , Helper.UseUncertaintyForAssumption]   
class World :
    def __init__ (self,_canvas,_subobject,goalAtom, helper = []) :
        
        self.canvas = _canvas
        self.areas = {} #{} #[[]]
        self.morphs = {}
        
        
        state = self.canState(_subobject) #newState(self,_subobject,(1,1)) #
        
        goalstate = self.canState(goalAtom)
        elim =  GoalStateEliminator(goalstate)
        self.molecules = [self.canMolecule(state,elim)]
        self.assCnt = 0
        self.implications = []   
        self.drawimplications = {False : [] , True : []}             
        self.drawingConstraints = {}
        #self.focus = 0
        self.helper = stdHelper + helper
        
    

    def existsCompMorphs(self,s,t)  -> bool :
        sout = self.out(*s)
        if (s == t) : 
            return True
        if (len(sout) == 0) :
            return False
        else :            
            return any (map (lambda s2 : self.existsCompMorphs(s2,t), sout))
    def addArea(self,x,y,width=stdWidth,height=stdHeight,exactHori=True,c=None,drawPnts = False) :
        #(x,y) = atom.room
        
        if (c == None) :
            c =Bsc.get_random_color()
            
        if (not (x,y) in self.areas) :
            #print(x,y,c)
            #print("addArea" , x,y)
            #print(getWidth(x, y))
            self.areas[(x,y)] = Area.Area(self.canvas,c,Bsc.getWidth(x,y),width,height,exactHori,drawPnts=drawPnts) #[(x,y)] = c #[x].append(a)
    def addSubArea(self,room,subRoom,d,frac,c=None,drawPnts=False) :
        if (c == None) :
            c = Bsc.get_random_color()
        self.areas[subRoom] =Area.SubArea(self.areas[room],d,frac,self.canvas,c,Bsc.getWidth(*room),True,drawPnts = drawPnts)
        self.drawingConstraints[(subRoom)] = (Atom.Atom(room , d ,  Ker) )
        self.addMorphism(*subRoom,*room,prop=Morphism.Mono)
    def addSES(self,room,d,frac,c=None) :
       if not (room in self.areas.keys()) : 
           if d == Hori : 
               wi = stdWidth # *1.5
               he = stdHeight
           else :
               wi = stdWidth
               he = stdHeight #* 1.5
           self.addArea(*room,width=wi,height=he,drawPnts=False)
           
       subRoom = Atom.Atom(room, d,Im).getCoRoom()  
       self.addSubArea(room,subRoom,d,frac,c,drawPnts=False)
       self.addCokernel(*subRoom,*room,drawPnts=True)


       #TODO
       #quotRoom = Atom.Atom(room,d,Ker).getCoRoom()

        
        
    def safeMax(self,kwargs) :# returns None if the 
        m = self.maximum(kwargs)
        for p in kwargs :
            if not self.existsCompMorphs(p , m) :
                return None
        return m
    def setUncPart(self,uncPart) : 
        self.uncPart = uncPart
        self.uncPart.repeat_every_second()
    def maximum (self,kwargs) : 
        xs = max ([x for (x,y) in kwargs]) #kwargs[::2]
        ys =max ([y for (x,y) in kwargs]) #kwargs[1::2]
        
        return (xs , ys)
    def minimum (self,kwargs) :
        xs = min ([x for (x,y) in kwargs]) #kwargs[::2]
        ys =min ([y for (x,y) in kwargs]) #kwargs[1::2]
        return (xs,ys)
    def applyAss(self,soft=True,onlyMonos=True) : # if soft is false this uses drawing constraints to refine the currect mm 
        s = self.mm().subobject().atom
        u = self.mm().uncertainty().atom
        print(s,u)
        bs = []
        bu = []
        #print("checking asses")
        impl = self.implications + self.drawimplications[True] + self.drawimplications[False] #todo
        if (not soft) : 
            impl = self.drawimplications[True]
            if not onlyMonos : 
                print("adding epis")
                impl += self.drawimplications[False]
        print("onlyMonos",onlyMonos,len(impl))
        for i in impl :
            (a,b) = i
            print(str(a) , "->" , str(b))
        for i in impl : 
            #print(i)
            (a,b) = i
            
            if a.isBiggerThan(s) :

                # one should be able to get to original state back TODO
                bs.append(b)
            if (b.isKernel(self) and a.isKernel(self))  and a.isBiggerThan(u) and Helper.UseUncertaintyForAssumption in self.helper :
                #print("lol")
                bu.append(b)
        #print(len(bs),len(bu))
        if (self.assCnt < len(bs + bu) ) :
            l = len(bs)
          
            if (self.assCnt < l) :                        
                    self.mm().updateStateFromSubobj(bs[self.assCnt])      
                     
            else :
                print("Updating uncertainty by assumption")
              
                self.mm().UP.updateAtom(bu[self.assCnt - l])
              
                #self.mm().draw
            self.assCnt += 1
            if (not soft and self.assCnt < len(bs + bu)) : 
                #print("next round")
                self.applyAss(soft)     
        
        else :            
                if soft and self.assCnt > 0 :
                    self.assCnt = 0
                    self.applyAss()

    def exactList(self,room)                : 
        el = self.areas[room].exactList()
        dele = []
        for d in el :           
            b = False
            for inf in [Ker, Im] :
                if not (b or (Atom.Atom(room,d,inf).getCoRoom() in self.areas.keys())) :                    
                    dele.append(d)                    
                    b = True
        for d in dele : 
            el.remove(d)
        return el
    def addCokernel(self ,x1, y1 ,x2 , y2,drawPnts=False) : 
        """(x1,y1) = src
        (x2,y2) = trg"""
        #,y1,x2,y2)
        newpos = (2 * x2 - x1 , 2 * y2 - y1)
        

        self.addMorphism(x2,y2,*newpos,prop = Morphism.Epi,drawProp=True,drawPnts=drawPnts)
    def addKernel(self,x1,y1,x2,y2,drawPnts=False) :
        newPos = (2 * x1 - x2 , 2 * y1 - y2)
        self.addMorphism(*newPos,x1,y1,prop= Morphism.Mono , drawProp=True,drawPnts=drawPnts)
    def printMMHistory(self) :
        print(self.mm().getHistory())
    def getMMIndex(self) : 
        return len(self.molecules) - 1
    def showMolecules(self) : 
        print("______________")
        for m in self.molecules :
            print (m)#,m.UP.printHistory())
        print("______________")
    def morPropToImp(self) :
        epis = [ value for key, value in self.morphs.items() if value.prop== Morphism.Epi]
        monos = [value for key, value in self.morphs.items() if value.prop == Morphism.Mono]
        for e in epis :
            self.drawimplications[False].append((FullOrZeroAtom(e.subobject().room, Full) , e.subobject()))
        for m in monos : 
            self.drawimplications[True].append(( m.subobject() , FullOrZeroAtom(m.subobject().room, Zero) ))
          
    def subobjectAtom(self) :
        return self.mm().subobject().atom
    def move(self,forward,d) :
        
        self.mm().move(forward,d)
        self.assCnt = 0
        
    def addMorphism(self,xs,ys,xt,yt,prop="",specialDir = "",drawProp = False, extra = [],drawPnts=False) :
        drawingConstraints = None
        d = self.getMdir(xs,ys,xt,yt)
       
        if (drawProp and prop == Morphism.Mono) : 
            
            self.drawingConstraints[(xs,ys)] = (Atom.Atom((xt,yt) , d ,  Ker) )
        
        if (prop != "") : 
            print(prop , (xs,ys) , (xt,yt))
        self.addArea(xs,ys,drawPnts=drawPnts)
        if (drawProp) : 
            if prop == Morphism.Epi :
                trg = Atom.Atom((xs,ys) , d, Coker)
                #print("drawConstr : " , trg)
                self.drawingConstraints[xt,yt] = trg           
                #drawingConstraints = Atom.Atom(d)
        self.addArea(xt,yt,drawPnts=drawPnts)        

        self.morphs[(xs,ys,xt,yt)] = self.genMor((xs,ys),(xt,yt) ,  prop)
        if Coker in extra : 
            #print("adding cokernel")
            self.addCokernel(xs,ys,xt,yt,drawPnts=drawPnts)
        if Ker in extra :
            self.addKernel(xs,ys,xt,yt,drawPnts=drawPnts)
    def swapFocus(self) :
        self.mm().swapFocus()
        print("swapping focus to" , self.mm().focus)
    #def focusTo(idx : int) :

    def finAll(self) :
        for m in self.molecules : #[::-1] :
            m.fin()
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
        print("Assumption: " , assAtom , " inside " , impAtom.showDirInf() )
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
    
    def createCoker(self,x2,y2,x1,y1) :
        #print("create coker" , x2 , y2 , x1 , y1)
        return self.areas[(x2,y2)].compQuotient(self.createImg(x2,y2,x1,y1))
    def createImg(self,x2,y2,x1,y1,unc=False):
        
        ax = self.areas[(x1,y1)]
        ay =self.areas[(x2,y2)]
        d = self.getDir(x1,y1,x2,y2)
        if len(d) > 1 :
            if (x1+1,y1) in self.drawingConstraints.keys() :
                d = d[1]
            elif (x1,y1+1) in self.drawingConstraints.keys() :
                d = d [0]
        
        # how to draw the img of a diagonal map, where the horizontal map is an explicit embedding?
        #print(x1,y1,x2,y2,d)
        segs = ax.findAllSegments(d)
        
        sidx = 0
        tidx = len(segs) - 1
        #print(segs)
        abort = False
        while (not (abort or Bsc.inList(segs[sidx].src() , ay.getPoints() , Bsc.comPnts))) :
            sidx +=1
            if (sidx == len(segs)) : 
                raise Exception("sidx Error!")
                sidx -= 1
                abort = True
            
        #print(tidx,segs[tidx])
        while (not (Bsc.inList(segs[tidx].trg() , ay.getPoints() , Bsc.comPnts))) :
            tidx -=1
            if (tidx <= 0 ) : 
                    raise Exception("tidx Error!")
                    break 
        
        segs = segs[sidx:tidx+1] #list(filter(lambda s : Bsc.inList(s.src() , ay.getPoints() , Bsc.comPnts) ,  ))
        
        xstart = (segs[0].x1,segs[0].y1)
        xendidx = len(segs)-1

        xend = (segs[xendidx].x2,segs[xendidx].y2)
        while ((not (Bsc.inList(xend , ay.getPoints() , Bsc.comPnts)))) :
            xendidx -= 1
            print("inc")
            xend = (segs[xendidx].x2,segs[xendidx].y2)
        #istart = list(filter (lambda  i : Bsc.comPnts(ay.segments[i].src() , xend) ,  range(len(ay.segments))))
        istart = list(filter (lambda  i : Bsc.comPnts(ay.segments[i].src() , xend) ,  range(len(ay.segments))))
        iend = list(filter (lambda i : Bsc.comPnts(ay.segments[i].trg() , xstart) , range(len(ay.segments))))
        if (len(istart) * len(iend) == 0) :
            raise Exception("create image error" )
        else :
            if (len(istart) != 1):
                print ("weird s",[str(ay.segments[i]) for i in istart])
            if (len(iend) != 1) :
                print ("werid end")
            istart = istart[0]
           
            iend =iend[0]   +1
            
            if (dirToMdir(d) == Diag) :#weird bug : 
                
                iend -= 1 ## if you know better fix, feel free
            
            segs2 = getSubList(istart,iend,ay.segments)
            
            img= Area.Area(self.canvas,ay.c,ay.w*2) #1.5)
            for s in segs + segs2 :
                img.stealSegment(s)
                    
            return img        
    def drawPntsOfArea(self,key) :
        self.areas[key].drawPnts = True
        self.areas[key].drawPoints()
    def isKernelZero(self,x1,y1,x2,y2) :
        b = False
        if (x1,y1) in self.drawingConstraints.keys() :
            if self.drawingConstraints[(x1,y1)] == Atom.Atom((x2,y2) , self.getMdir(x1,y1,y2,y2) , Ker) :
                #print("createker",x1,y1,x2,y2,"solved by drawingCons")
                b = True        
        return (x1,y1) == (x2,y2) or b 
    def isZero(self, s : Atom) :
        return (s.info == Zero) or (s.info == Ker and self.isKernelZero(*s.room,*s.getCoRoom()))
    def refineMM(self,onlyMonos) :
        #iszero = self.isZero(self.mm().subob)
        #if iszero : return Atom.FullOrZeroAtom(s.room,"Zero")
        self.applyAss(False,onlyMonos)
        
    def createker(self,x1,y1,x2,y2,unc = False):
        
        if self.isKernelZero(x1,y1,x2,y2) :
           a = self.areas[(x1,y1)]
           zero = Area.Area(self.canvas,"black", a.w * 0.1,a.width,a.height )
           for s in a.segments :
               zero.stealSegment(s)
           return zero
        else :
            return self.areas[(x1,y1)].comp(self.createImg(x2,y2,x1,y1),unc=unc)
    def jumpback(self) :
        self.mm().jumpback()
    def removeFromList(self,molc) : 
        self.molecules.remove(molc)
    def canMolecule2 (self, SP ,  uncAtom , _eliminator) :
        _goalState = _eliminator.targetState
        #print("creating can Molecule")
        
        UP =  lambda mol: Particle.Particle(mol,uncAtom,Genus.Unc,_goalState)

        focus = Genus.Sub
        return Molecule(self,_eliminator,SP , UP) #,initAreas = True)
    def canMolecule ( self,_state ,_eliminator) :
        #self.state = State()
        #self.wld = _wld
        _goalState = _eliminator.targetState
        #self.eliminator = _eliminator
        
        #print("creating can Molecule from state" , _state)
        SP = lambda mol : Particle.Particle(mol,_state.subobject,Genus.Sub,_goalState)
       
        focus = Genus.Sub
        return self.canMolecule2(SP , _state.uncertainty , _eliminator) #Molecule(self,_eliminator,SP , UP)
        
    def subobject(self) :
        return self.mm().subobject()
    def canState (self,_subobject) :
            return newState(self,_subobject,_subobject.room)   
    

    
    def drawAreas(self) :
        for coords in self.areas.keys() :
            #if (coords in [(-1,0),(0,1)]):
            #print("drawing", coords,len(self.areas[coords].segments))
           
                self.areas[coords].drawSegments()
    def genMor(self,s,t,p) :
        #print("generate" ,s , "-",  p , "->"  , t )

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
            if len(o) >= 2 and False : #todo
                t = self.maximum(o)
                
                curveDR = not (any(map(lambda s : self.genMor(s,t,Morphism.Epi).inList(self.morphs.values()) , o)))
                
            if len(i) >= 2 and False :
                s = self.minimum(i)
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
            if (coords in self.drawingConstraints.keys()) :
                    a = self.areas[coords]
                    if (isinstance(a,Area.SubArea))     :
                    #äprint("subinit")
                        a.subInitialize(st)
                    else :
                        dC = self.drawingConstraints[coords]
                    
                        self.areas[coords] = dC.getArea(self)

                        #print(self.areas[coords].getPoints())
                        
                    #self.areas[coords].initialize()
                #print("adding area by constraint: " , self.drawingConstraints[coords])
            else :
                    a = self.areas[coords]                
                    insWidth = 0
                    insHeight = 0
                    y2 = y
                    for x2 in range(x) :
                        while not ((x2,y2) in self.areas.keys()) :
                            y2 -= 1

                        a = self.areas[(x2,y2)]
                        insWidth += a.width * (a.rightFrac) 
                    x2 = x
                    for y2 in range(y) : 
                        while not ((x2,y2) in self.areas.keys()) :
                            x2 -=1
                        a = self.areas[(x2,y2)] 
                        insHeight += a.height * (a.downFrac)
                    
                    self.areas[coords].initialize(originX + insWidth -  w / 2 * (x +y),
                            originY + insHeight -  w / 2* (x + y),
                            a.width +  w  * (x +y)  ,a.height +  w  * (x +y),st)
            if self.areas[coords].drawPnts : self.areas[coords].drawPoints()
                    #self.areas[coords].drawPoints()
        self.mm().initState() 
        self.morPropToImp()