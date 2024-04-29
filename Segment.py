#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 12:18:10 2024

@author: tim

"""
import BasicFunctions as Bsc

def strEq(str1,str2):
    return (Bsc.sorted(list(str1)) == Bsc.sorted(list(str2)))
    

class Segment :
    def copy(self) :
        return Segment(self.canvas,self.x1,self.y1,self.x2,self.y2,self.style,self.w,self.c)
    def invert(self) :
        return Segment(self.canvas,self.x2,self.y2,self.x1,self.y1 , self.style,self.w,self.c)
    def __str__ (self) :
        return str(round(self.x1)) + " " + str(round(self.y1)) + "->" + str(round(self.x2))+ " " + str(round(self.y2))
    def __init__ (self,_canvas,_x1,_y1,_x2,_y2,_style,_w,_c,_glue = False):
        self.x1 = _x1
        self.x2 = _x2
        self.y2 =_y2
        self.y1 = _y1
        self.style = _style
        self.canvas = _canvas
        self.w = _w
        self.c = _c
        self.dir = "Undetermined"
        self.id = None
        self.glue =_glue
        #print(_w)
    def draw(self) :
        if self.style == "line" :
            #w = self.w
            self.id = self.canvas.create_line(self.x1,self.y1,self.x2,self.y2,width = self.w,fill=self.c)
        else:
            a = whichArcPos(self.style, self.x1 , self.y1, self.x2,self.y2)
            
            if (not a == "") :
                r = abs(self.x1-self.x2)
                if (self.style == "DR"):
                    if Bsc.so(a) == Bsc.so("SO"):
                        self.id =  self.canvas.create_circle_arcDR(self.x2,self.y2,r,outline=self.c,width=self.w)        
                    if Bsc.so(a) == Bsc.so("SW"):
                        
                        self.id =  self.canvas.create_circle_arcDR(self.x1,self.y1,r,outline=self.c,width=self.w)        
                else :
                    if Bsc.so(a) == Bsc.so("NW"):
                        self.id =  self.canvas.create_circle_arcUL(self.x1,self.y1,r,outline=self.c,width=self.w)        
                    if Bsc.so(a) == Bsc.so("NO"):
                        self.id =  self.canvas.create_circle_arcUL(self.x2,self.y2,r,outline=self.c,width=self.w)        
            else: 
                    print("radius mismatch!")
        
    def enlarge(self,x2n,y2n) :
        self.x2 = x2n
        self.y2 = y2n
    def erase(self) :
        
        self.canvas.delete(self.id)   
    def src(self) :
        return (self.x1,self.y1)
    def trg(self) :
        return (self.x2,self.y2)
    
def whichArcPos(style,x1,y1,x2,y2) : 
   r = x2 - x1
   r2 = y2 - y1
   
   if (abs(abs(r) - abs(r2))<2) :     
       if (r > 0 and style == "UL") : return "NW"
       if (r < 0 and style == "DR" ) : return "SO"
       if (r < 0 and style =="UL") : return "ON"
       if (r > 0 and style == "DR") : return "WS"

              
   else:
        print("this is not an arc")
        return ""
def HoriVertiArc (style,x1,y1,x2,y2):
    if style == "line":
        if (y1 == y2) : return "H"
        if (x1 == x2) : return "V"
    else:
        return whichArcPos(style,x1,y1,x2,y2)
