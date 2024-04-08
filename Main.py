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
from Atom import Hori , Verti, Diag
from Morphism import Mono, Epi
import State
import Atom
import BasicFunctions as Bsc


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
def viererMono() :

    so =  Atom.Atom((2,0),Atom.Verti,Atom.Ker) # Atom.FullOrZeroAtom((2,0),"Full")
    go =Atom.FullOrZeroAtom((3,1),Atom.Zero) # Atom.Atom((3,1) , Atom.Hori, Atom.Ker) #Atom.FullOrZeroAtom((2,0),Atom.Zero)
    wld = World.World(canvas, so , go )

    wld.addMorphism(0, 0,0, 1 ,Epi)
    wld.addMorphism(0, 0,1,0)
    wld.addMorphism(1,0, 2, 0)

    #wld.addArea(x, y)
    wld.addMorphism(1, 0,1,1,Mono)
    wld.addMorphism(0,1,1,1)
    wld.addMorphism(1,1,2,1)


    wld.addMorphism(2, 0, 3, 0)# ,Mono)
    wld.addMorphism(2,0,2,1,Mono)

    wld.addMorphism(2, 1, 3, 1)
    wld.addMorphism(3,0,3,1,Mono)
    return wld
def epiIntro() :
    so =Atom.FullOrZeroAtom((1,0),"Full")
    go = Atom.Atom((1,0),Atom.Hori,Atom.Im)
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1)
    
    wld.addMorphism(0,0,1,1)
    wld.implications.append((Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im)))
    wld.implications.append((Atom.Atom((1,1),Atom.Verti,Atom.Im) , Atom.Atom((1,1),Atom.Diag,Atom.Im)))
    return wld
def kernelInc() :
    so =  Atom.Atom((0,0),Atom.Diag,Atom.Ker)
    go = Atom.Atom((0,0),Atom.Hori,Atom.Ker)
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1,Mono)
    
    wld.addMorphism(0,0,1,1)
    return wld
    #wld.implications.append((Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im)))
    #wld.implications.append((Atom.Atom((0,0),Atom.Diag,Atom.Ker) , Atom.Atom((0,0),Atom.Hori,Atom.Ker)))
def monoIntro() :
    so =  Atom.Atom((1,0),Atom.Verti,Atom.Ker)
    go =Atom.FullOrZeroAtom((1,0),"Zero")
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1)
    
    wld.addMorphism(0,0,1,1)
    wld.implications.append((Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im)))
    wld.implications.append((Atom.Atom((0,0),Atom.Diag,Atom.Ker) , Atom.Atom((0,0),Atom.Hori,Atom.Ker)))
    return wld
wld = kernelInc() #viererMono() epiIntro() #
wld.initialize()


wld.drawAreas()
wld.mm().draw()

chars = ['w','a','s','d','c','q','f','x','p','j']
funcs = [lambda : wld.move(False,Verti) , lambda : wld.move(False,Hori) , lambda : wld.move(True,Verti) , lambda : wld.move(True,Hori) , 
         lambda : wld.move(True,Diag) , lambda : wld.move(False,Diag) , wld.applyAss , wld.finMM, wld.swapFocus , wld.jumpback]



def key_pressed(event):
    
    r = event.char
    i = Bsc.get_indices(chars,r) 
    #print(i,r,r in chars)
    if not wld.gameEnd()  :
        if (len(i) > 0) :
            funcs[i[0]]()
            #print("Key pressed:", )


tk.title("Key Listener")

# Bind the key press event to the key_pressed function
tk.bind("<Key>", key_pressed)
#but2 = tkr.Button(frame, text="erase", command=wld.)

#but2.grid(row=1,column=0)
#but.pack()
tkr.mainloop()
