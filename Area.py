#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:19:32 2024

@author: tim
"""
import Segment
import BasicFunctions as Bsc
import tkinter as tkr
import random
import Atom 
import numpy as np
import sys
sys.path.append("./anaconda3/lib/python3.9/site-packages")
from shapely.geometry import Point, Polygon

class Area : 
     def __init__ (self,_canvas,_c : str,_w : int ,_width : int =None, _height : int =None,_exactHori = True,_filled =False, ordinary = True, drawPnts = False)  :
         self.canvas = _canvas
         self.w = _w
         self.c = _c
        # print("init:",self.c)
         self.segments = []
         self.exactHori = _exactHori
         self.mp = None
         self.filled = _filled
         self.fillArea = None
         self.initFracs()
         self.width = _width
         self.height = _height
         self.x = None
         self.y = None
         self.ordinary = ordinary
         self.drawPnts = drawPnts
     def addSub(self, d, frac) :
         if (frac > 1 / 2) : 
             self.oversizeFrac = True
             frac = 1 - frac
         if (d == Atom.Hori) :
             self.leftFrac = frac
             self.initRightFrac()
         else : 
             raise ("add verti sub")
             self.upFrac = frac
             self.downFrac = 1 - frac
     def addQuot(self,d,frac) :
         return
         #todo #if (d == Atom.Hori) : 
             
     def create_segments (self,style, *kwargs,glue=False):
        #print(kwargs,len(kwargs))
        segs = [[kwargs[i], kwargs[i+1],kwargs[i+2],kwargs[i+3]] for i in range(0, len(kwargs)-2, 2)]
        #directs = ["N"]
      
        for i in range(len(segs)) :
            #print("start",i)
            if (segs[i][0],segs[i][1]) != (segs[i][2],segs[i][3]) :
               # if glue : 
                   # self.segments[-1].enlarge(segs[i][2] , segs[i][3]) 
               # else :
                    
                    if (len(self.segments) > 0) : 
                        if not Bsc.comPnts(self.segments[-1].trg() , (segs[i][0] , segs[i][1])) :
                            print("seg append didnt fit")
                    self.segments.append(Segment.Segment(self.canvas,*segs[i],_style=style,_w = self.w,_c = self.c,_glue=glue)) #,_dir = direct[i]) )
     def stealSegment (self,seg) :
        if (isinstance(self,SubArea)) : 
            raise ("well")
        #print("stealing",seg)
        s = seg.copy()
        s.c = self.c
        s.w = self.w #*= 1.5
        #print("stealing a segment from len", len(self.segments) , ":" , s)
        self.segments.append(s)                    
     def generateDirections(self) :
        direct= []
        def core (nhv , hvlab , nhvp , direct , glues, hv) :
            j = 0
            for i in range(len(nhv)):#hlab[nhp]
                
                n = direct[nhv[i]] 
                if n == hv :
                    
                    if (glues[nhv[i]]) :
                        #print("h glues")
                        j +=1
                         
                        #direct[nh[i]] = direct[nh[i]-1]
                        
                    
                    direct[nhv[i]] = hvlab[nhvp][i-j]  
                else :
                    h = hlab[nhp][i-j]
                    if (Bsc.so(n) != Bsc.so(h)) :
                        print(n,h,"something went wrong")
        direct = [Segment.HoriVertiArc(p.style,p.x1,p.y1,p.x2,p.y2) for p in self.segments]
        glues = [p.glue for p in self.segments]
        #print(direct)
        nh = Bsc.get_indices(direct, "H","SO","NW")
        nV = Bsc.get_indices(direct, "V","SO","NW","ON","WS")
        hlab = [["N","S"],["NO","SO","SW","NW"],["NO","SO","S","SW","NW","N"]]
        vlab = [["O","W"],["ON","OS","WS","WN"],["ON","O","OS","WS","W","WN"]] ## renamed OS to SO
        nhp = int(len(nh) / 2) -1
        nVp = int(len(nV) / 2)  - 1
        #nhp = max(nhp,nVp)
        #nVp = max(nhp,nVp)
        core(nh,hlab,nhp,direct,glues,"H") 
        #print(direct)
        core(nV , vlab , nVp , direct, glues,"V")
       
        
        #print(direct)
        for i in range(len(self.segments)):
            self.segments[i].dir = direct[i]
     def getPoints(self) : 
             return [s.src() for s in self.segments]     
     def getPointsAsNumberList(self) : 
         p = []
         for s in self.segments :
             (x,y) = s.src()
             p = p + [round(x),round(y)]
         #print(p)
         return p
     def drawPoints(self) : 
         for seg in self.segments :
             r = 30
             if (seg == self.segments[0]) :
                 r = 50
             self.canvas.create_circle_arc(seg.x1,seg.y1,r,start = 0,end = 359,fill=self.c)
     def showSegments(self) :
        st = ""
        for s in self.segments :
            st += str(s) + " | "
        print(st)
     def drawSegments (self):
        
        #print("number of segs to draw", len(self.segments))
        for seg in self.segments :
            seg.draw()
        if self.filled :
            if (self.ordinary)  :
                self.fillArea = self.canvas.create_polygonWithAlpha(*(self.getPointsAsNumberList()),fill=self.c , alpha=0.5) #='#0070c080')"#ff000055")# #self.c,
     def segmentFromDirection(self , d) :
        self.generateDirections()
        l = list (filter(lambda s : Bsc.so(s.dir) == Bsc.so(d) , self.segments))
        if (len(l) > 0) :
            return l[0]
        else  :
            print("segment with direction " , d , " not found")
     def getMiddlePoint(self , offSet = 0) :
         pts = self.getPoints()
         
         (x1,y1) = pts[0]
         (x2,y2) = pts[0]  #segmentFromDirection("SW").trg()
         for p in pts :
             (x,y) = p
             if (x - y > x1 - y1) :
                 (x1,y1) = (x,y)
             if (y - x > y2 - x2) :
                 (x2 , y2) = (x,y)
         
         
         x = (x1 + x2) /2 + offSet
         y = (y1 + y2) /2 + offSet
         return (x,y)
     def drawAndReturnZeroArea(self) :
         return self.canvas.create_circle_arc(*self.getMiddlePoint(30),20,start = 0,end = 359)
     def drawMiddlepoint(self) :
         if self.ordinary :
            self.mp = self.canvas.create_circle_arc(*self.getMiddlePoint(),20,start = 0,end = 359,fill=self.c)
         #self.mp = self.canvas.create_circle_arc(x2,y2,20,start = 0,end = 359,fill="blue")
     def eraseSegments(self) :
         
         for seg in self.segments :
         
             seg.erase()    
         if (self.mp != None) :
             self.canvas.delete(self.mp)
         if (self.filled) :
             self.canvas.delete(self.fillArea)
         if (not self.ordinary) :
             self.canvas.delete(self.area)

         self.segments = []
         self.canvas.update()
  
     def findAllSegments(self,d,invert=False):
        self.generateDirections()
        ret = []
        for s in self.segments :
            if invert :
                if (not (Bsc.subList(Bsc.so(d) , Bsc.so(s.dir)))) :
                    ret.append(s)
            else :
                if (Bsc.subList(Bsc.so(d) , Bsc.so(s.dir))):
                    ret.append(s)
        return ret
     def getSegIdxByTrg(self, trg) :
         l = list(filter (lambda  i : Bsc.comPnts(self.segments[i].trg() , trg) ,  range(len(self.segments))))
         if (len(l) > 0) :
             return l[0]
         else :
             return -1
     def getSegIdxBySrc(self, src) :
           l = list(filter (lambda  i : Bsc.comPnts(self.segments[i].src() , src) ,  range(len(self.segments))))
           if (len(l) > 0) :
               return l[0]
           else :
               return -1
     def compQuotient(self , sub) : # unc is always false, the uncertainty is never a cokernel
        # print("creating compquotient" , self , sub)
     
         
         w = self.w * 1.5
         c = self.c
        
         comp = Area(self.canvas,c,w )
         i = 0
         """print("sub:")
         sub.showSegments()
         print("____________\n self:")
         self.showSegments()"""
         #for s in sub.segments : print(s) 
         #for s in self.segments : print(s) 
         idx = sub.getSegIdxByTrg(self.segments[i].trg())
         #
         
         #print("checking now" , self.segments[i] , "has" , idx)
         while (idx != -1) :       # finding first self-segment not contained in sub                  
             i += 1
             idx = sub.getSegIdxByTrg(self.segments[i].trg())
         #print("erstes self-segment not contained in sub hat idx" , i)
         #print("segments before critical")
         #comp.showSegments()
         while (idx == -1) :
             comp.stealSegment(self.segments[i]) #maybe put this before while
             
             i += 1
             idx = sub.getSegIdxByTrg(self.segments[i].src())
          #   print("i,idx",i,idx)
         
         j = self.getSegIdxBySrc(sub.segments[idx].src())
         #print("j,idx",j,idx)
         
         comp.stealSegment(sub.segments[idx].invert()) 
         #print("j,idx",j,idx)
         #j = self.getSegIdxBySrc(quot.segments[idx].src())
         idx -= 1
         
         while (j == -1) :
            
            comp.stealSegment(sub.segments[idx].invert()) 
            
            #print("j,idx",j,idx)
            j = self.getSegIdxBySrc(sub.segments[idx].src())
            idx -= 1
            
         #comp.stealSegment(sub.segments[idx].invert())
            
         
        # for i in range(j,len(self.segments)) :             
        #        comp.stealSegment(self.segments[i])
         """print("final coker:")
         comp.showSegments()
         print("_____")"""
         return comp
        
     def comp (self, quot,unc=False) :
         
         w = self.w * 1.5
         c = self.c
         #print([str(s) for s in quot.segments])
         if (unc) :
            w = self.w / 2
            c = "black"
         #unc = False 
         comp = Area(self.canvas,c,w )
         i = 0
         idx = quot.getSegIdxByTrg(self.segments[i].src())
         #print("i,idx",i,idx)
         nunc = not unc
         while (idx == -1) :
             
             if (nunc) : comp.stealSegment(self.segments[i])
             i += 1
             idx = quot.getSegIdxByTrg(self.segments[i].src())
          #   print("i,idx",i,idx)
         
         j = self.getSegIdxBySrc(quot.segments[idx].src())
         #print("j,idx",j,idx)
         
         comp.stealSegment(quot.segments[idx].invert()) 
         #print("j,idx",j,idx)
         #j = self.getSegIdxBySrc(quot.segments[idx].src())
         idx -= 1
            
         while (j == -1) :
            
            comp.stealSegment(quot.segments[idx].invert()) 
            
            #print("j,idx",j,idx)
            j = self.getSegIdxBySrc(quot.segments[idx].src())
            idx -= 1
            
            
            
         if nunc :
             for i in range(j,len(self.segments)) :             
                comp.stealSegment(self.segments[i])
         return comp
        
     def exactList(self) :
         a = [Atom.Verti]
         if self.exactHori :
             a.append(Atom.Hori)
         return a
    #  def getRightFrac(self) :
    #     if self.exactHori :
    #         self.rightFrac =  1 - self.leftFrac         
    #     return self.rightFrac
     def initRightFrac(self,rf=1/2) : 
        self.rightFrac = rf
        if self.exactHori :
            self.rightFrac =  1 - self.leftFrac  
     def random_Point_in_Polygon(self):
        polygon = Polygon(self.getPoints())
        minx, miny, maxx, maxy = polygon.bounds
        cnt = 0
        while cnt < 10000:
            pnt = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            if polygon.contains(pnt):
                return pnt

            cnt +=1         
        raise Exception("random point was not construtible")
     def initFracs(self) :
        self.leftFrac = 1 / 2
        self.upFrac = 1 / 2

        self.initRightFrac()
        self.downFrac = 1 - self.upFrac
     def initialize(self,x,y,width,height,arcs) : # width height werden nochmal übergeben, wegen width changes.
      # this function dra
      # ws the segments starting from leftFrac and upFrac.
       
       # print("start init")
        _min= min(width,height)
        #print(_min == height)
        if (self.leftFrac == 0) :
            _min = height
        if (self.upFrac == 0) :
            _min = width
        #print(arcs)
        self.x = x
        self.y = y
        leftFrac2 = self.leftFrac
        upFrac2 = self.upFrac
        
        self.create_segments("line",    x+ width - leftFrac2*_min ,y, x+width , y)
        st = "line"
        if ("NO" in arcs) :
            st = "UL"
        self.createArc(x + width , y , x + width , y + _min * self.upFrac,st)
        
        self.create_segments("line",x + width , y + _min * self.upFrac , x + width , y + height - _min * upFrac2)
        if ("SO" in arcs) :
            st = "DR"
            
        else : 
            st = "line"
        self.createArc(x + width , y + height - _min * upFrac2 , x +width - _min * leftFrac2 , y+ height,st)
        self.create_segments("line",x +width - _min * leftFrac2 , y+ height, x + _min * self.leftFrac , y+ height,x,y+height)
        #In the previous line there is an issuefor subobjects because _min is not height, so 2 interior nodes on the vertical axes are produced.
        if ("SW" in arcs) : 
            st = "DR" 
        else :
            st = "line"
        self.createArc(x  , y+ height , x , y + height - _min * upFrac2,st)
        self.create_segments("line",x , y +height - _min * upFrac2, x ,y + _min * self.upFrac)
        if ("NW" in arcs):
            
            st = "UL"
        else:
            st = "line"
        #print("segments before critical",leftFrac2)
        #self.showSegments()
        
        #print("upf",self.upFrac)
        if (self.leftFrac <= 1/2 ) : #new 
            self.createArc( x ,y + _min * self.upFrac,x + _min * self.leftFrac,y,st)
            self.create_segments("line",x + _min * self.leftFrac,y,x + width - _min*leftFrac2,y)
        else :
            
            #print(x ,y + _min * self.upFrac,x + _min * self.leftFrac,y)
            #print(x + _min * self.leftFrac,y,x + width - _min*leftFrac2)
            #self.create_segments("line", x ,y + _min * self.upFrac,x,y)
            #self.create_segments("line",x,y,x + _min * self.leftFrac,y)
            #self.create_segments("line",x + _min * self.leftFrac,y,x + width - _min*leftFrac2,y)
            self.createArc( x ,y + _min * self.upFrac,x + width - _min*leftFrac2,y,st)
            #self.create_segments("line",x + _min * self.leftFrac,y,x + width - _min*leftFrac2,y)
            
        if self.drawPnts : self.drawPoints()


def isSpecialArc(style,x1,y1,x2,y2):
        return style != "line" and x1 == x2
def _createArc(self,x1,y1,x2,y2,style) :     
   if style == "line":
        if (x1 == x2 or y1 == y2):
            self.create_segments("line",x1,y1,x2,y2) 
        else:
            self.create_segments("line",x1,y1,x1 , y2 , x2 , y2)
   else:     
    if style == "DR" : 
        vorz = -1
    else :
        vorz = 1
    
    if (isSpecialArc(style,x1,y1,x2,y2)):
            r = y2 - y1
            #self.segments[-1].glue = True only for kernels
            self.create_segments("line",x1,y1,x1 + r,y1,glue="True") 
            if style == "DR" :
                
                #self.canvas.create_circle_arc(x1,y1 - vorz*r,30,start = 0,end = 359,fill="black")
                #self.canvas.create_circle_arc(x1 + r,y1,30,start = 0,end = 359,fill="red")
                self.create_segments(style,x1 + r,y1,x1,y1 - vorz *r)
            else :
                self.create_segments(style,x1 + r,y1,x1,y1 + vorz *r)
    else :
        self.create_segments(style,x1,y1,x2,y2)
        """if (x1 > x2) :
                self.create_segments("DR",x1,y1,x2,y2)
            else:
                self.create_segments("UL",x1,y1,x2,y2)"""
                
def _createArea(self,x,y,width,height,c,w,exactHori, *arcs):

    
    a= Area(self,_c=c,_w=w)
    if (a.segments != []) :
            raise Exception("segments are nonempty before!!!")
    a.initialize(x, y, width, height, *arcs)
            

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x-r, y-r, x+r, y+r , **kwargs)

Area.createArc = _createArc    
def _create_circle_arcDR(self, x, y, r, **kwargs):    
    kwargs["extent"] = 90
    return self.create_arc(x-r, y-2*r, x+r, y, start = 270,  style="arc", **kwargs)
def _create_circle_arcUL(self, x, y, r, **kwargs):

    kwargs["extent"] = 90 #kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x, y-r, x+2*r, y+r, start = 90, style="arc", **kwargs)


class SubArea(Area) :
    def __init__(self,_superArea : Area,_d,_frac,_canvas,_c,_w,_exactHori = True,_filled =False,drawPnts = False) :
        self.superArea = _superArea
        self.d = _d
        self.frac = _frac
        super().__init__(_canvas,_c,_w,_exactHori,_filled,drawPnts=drawPnts)
        _superArea.addSub(_d,_frac)
    def subInitialize(self,st) :
        if (self.d == Atom.Hori) : 
            wi = self.superArea.width * self.frac
            hi = self.superArea.height
            if (self.frac > 1/2) : 
                self.leftFrac = 1/2
                #self.upFrac = 1 / 2
            else :
                self.leftFrac = 0
            self.initRightFrac()
        else : 
            wi = self.superArea.width
            hi = self.superArea.height * self.frac 
            self.upFrac = 0
            self.downFrac = 0 #todo?
        #print(wi,hi)
            
        super().initialize(self.superArea.x,self.superArea.y,wi,hi,st)
       # print("Before:\n")
        #self.superArea.showSegments()
        self.superArea.segments = [self.superArea.segments[-1]] + self.superArea.segments[:-1]
        #self.showSegments()
        #todo
