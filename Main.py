#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:59:46 2024

@author: tim
"""

import tkinter as tkr
from tkinter import  ttk
import random
import Segment

import Area
import Atom
from Atom import Hori , Verti, Diag

import BasicFunctions as Bsc
from MovingUnc import MovingUnc
from PolygoneWithAlpha import create_alphaPoly
import threading
import time
import sys
import Levels
sys.path.append("./anaconda3/lib/python3.9/site-packages")
from shapely.geometry import Point, Polygon

"""
TODO : manchmal werden UNC nicht angezeigt für subareas. A -> B -> A , + f
"""
#w =6
tk = tkr.Tk()
frame = tkr.Frame(tk)
frame.grid(row=0, column=0)
canvas = tkr.Canvas(frame, width=1500, height=800)
canvas.grid(row=0,column=0)



def _createRect(self,x,y,width,height,c,w=6) :
    self.create_rectangle(x,y,x+width,y+height,outline=c,width=w)
    
                
#tkr.Canvas.showImg = _showImg
tkr.Canvas.createRect = _createRect
#tkr.Canvas.createRect2 = _createRect2
tkr.Canvas.create_circle_arc = Area._create_circle_arc
tkr.Canvas.create_circle_arcDR = Area._create_circle_arcDR
tkr.Canvas.create_circle_arcUL = Area._create_circle_arcUL
tkr.Canvas.createArea = Area._createArea 
images = []
def createPolygone(self, *args, **kwargs) : 
    #print("creating polygone")
    return create_alphaPoly(self,images,*args,**kwargs)
tkr.Canvas.create_polygonWithAlpha = createPolygone
#################################################################################################

wld = Levels.viererMono(canvas) # Levels.viererMono(canvas) #Levels.viererEpi(canvas) #  
uncPart = MovingUnc(tk,canvas,wld)
wld.setUncPart(uncPart)
#################################################################################################
wld.initialize()


wld.drawAreas()

wld.mm().draw()

chars = ['w','a','s','d','c','q',
        'f','x','p','j','m','h']
funcs = [lambda : wld.move(False,Verti) , lambda : wld.move(False,Hori) , lambda : wld.move(True,Verti) , lambda : wld.move(True,Hori) , lambda : wld.move(True,Diag) , lambda : wld.move(False,Diag) , 
         wld.applyAss , wld.finAll, wld.swapFocus , wld.jumpback, wld.showMolecules , wld.printMMHistory]



def key_pressed(event):
    
    r = event.char
    i = Bsc.get_indices(chars,r) 
    #print(i,r,r in chars)
    if not wld.gameEnd()  :
        if (len(i) > 0) :
            funcs[i[0]]()
            #print("Key pressed:", i[0])


tk.title("Diagram Chase")

# Bind the key press event to the key_pressed function
tk.bind("<Key>", key_pressed)
#but2 = tkr.Button(frame, text="erase", command=wld.)

#but2.grid(row=1,column=0)
#but.pack()

    
"""
def uncertaintyThread() :
    time.sleep(10000)
"""    
#t = threading.Thread(target=uncertaintyThread)
#t.start()

tkr.mainloop()
