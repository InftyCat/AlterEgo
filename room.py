#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:59:46 2024

@author: tim
"""

import tkinter as tkr
import random
import Segment
import World
import Area
import State

#w =6
tk = tkr.Tk()
frame = tkr.Frame(tk)
frame.grid(row=0, column=0)
canvas = tkr.Canvas(frame, width=1000, height=700)
canvas.grid(row=0,column=0)



def _createRect(self,x,y,width,height,c,w=6) :
    self.create_rectangle(x,y,x+width,y+height,outline=c,width=w)
    

#roundcoef = 1/2
#rinv = 1 - roundcoef
#def _createObj(self):
    #self.obj =

# ALWAYS GO clockwise around the area!
# right now i didnt implemented exactness with curves in a column.



    #x1,y1,x2,y2 = 0,0,30,30
    
    #self.coords(subobject,x1,y1,x2,y2)
    #subobject = self.createRect(200,200,50,50,fill="purple")


"""
def _createRect2(self,x,y,c,originX = originX,originY = originY,anzIn = 1, anzOut = 1,dl = False, ur = False) :
    
    
    
    st = []
    if anzIn == 2 and anzOut == 1 :
            
            st = ["NW"] #self.createRectUL
    elif anzIn == 1 and anzOut == 2  :
            st = ["SO"]
    else :
            st= []
    if dl:
        st.append("SW")
    if ur :
        st.append("NO")   
    #print(c,st)         
    w= 6
    return self.createArea(originX + x * (stdWidth / 2 ) -  w / 2 * (x +y),
               originY + y * (stdHeight / 2) -  w / 2* (x + y),
               stdWidth +  w  * (x +y)  ,stdHeight +  w  * (x +y),c,getWidth(x,y),True,*st)            
"""
                
           

                
#tkr.Canvas.showImg = _showImg
tkr.Canvas.createRect = _createRect
#tkr.Canvas.createRect2 = _createRect2
tkr.Canvas.create_circle_arc = Area._create_circle_arc
tkr.Canvas.create_circle_arcDR = Area._create_circle_arcDR
tkr.Canvas.create_circle_arcUL = Area._create_circle_arcUL

tkr.Canvas.createArea = Area._createArea        
wld = World.World(canvas, State.FullOrZeroState((0,0),"Full")) # State.State((0,0), State.Hori, State.Ker)) # State((2,0),State.Hori,State.Im)) # 
#wld.addArea(0,0)
def f () :
    #wld.deleteState()
    #canvas.delete(wld.subobject)
    wld.move(True,State.Hori)
    #wld.updateState(State.State((0,0), State.Hori, State.Ker))
    #wld.drawState()
    
wld.addMorphism(0, 0,0,1) # ,"Mono")
wld.addMorphism(0, 0,1,0)
wld.addMorphism(1,0, 2, 0)

#wld.addArea(x, y)
wld.addMorphism(1, 0,1,1) # ,"Epi")
wld.addMorphism(0,1,1,1)

wld.initialize()
wld.initSubArea()
wld.drawAreas()
wld.drawState()
"""
a00 = canvas.createRect2(0,0,'green' ,anzOut=2)#  ,ur=True,dl=True)
#a = canvas.createRect2(0,2,'green')
#a.drawPoints()

a01 = canvas.createRect2(0,1,"pink",ur=True)
a10 = canvas.createRect2(1,0,'purple',anzOut=2)
a11 = canvas.createRect2(1,1,'red',anzIn=2,ur=True)
#obj = canvas.create
canvas.createRect2(2,0,'cyan',anzOut=2,dl=True)
canvas.createRect2(2,1,'yellow',anzIn=2)

canvas.createRect2(3,0,'black',dl=True)
canvas.createRect2(3,1,'white',anzIn=2)
"""
#print(a.generateDirections())



but = tkr.Button(frame, text="test", command=f)

but.grid(row=1,column=0)
#but2 = tkr.Button(frame, text="erase", command=wld.)

#but2.grid(row=1,column=0)
#but.pack()
tkr.mainloop()
