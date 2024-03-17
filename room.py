#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:59:46 2024

@author: tim
"""
"""
from ipycanvas import Canvas
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel('fruit supply')
ax.set_title('Fruit supply by kind and color')
ax.legend(title='Fruit color')

#plt.show()

canvas = Canvas(width=200, height=200, sync_image_data=True)
canvas.stroke_rect (100,100,50,30)
#canvas.to_file("test.png")

canvas
"""
import tkinter as tkr
w =6
tk = tkr.Tk()
canvas = tkr.Canvas(tk, width=2000, height=1000)
canvas.grid()

def _createRect(self,x,y,width,height,c,w=w) :
    self.create_rectangle(x,y,x+width,y+height,outline=c,width=w)
    
stdWidth = 300
stdHeight = 300
originX = 100
originY = 100
maxX = 4
maxY = 1
roundcoef = 1/7
def _createRectDR(self,x,y,width, height,c , w=w) :
    _min= min(width,height)
    
    self.create_line(x,y, x+width , y ,x+width, y+ _min/3, width =w,fill=c)
    #canvas.create_arc(x+width/3, y+height/3, width * 2 / 3, style="arc", outline=c, width=6, start=270, end=360)
    #self.create_arc(x-width/3, y-height/3 , x+width , y +  height,start=270,extent = 90 , style="arc", outline=c, width=w) #,x+width, y+ height/3, 
    
    self.create_circle_arcDR(x+ width-2*_min/3 , y +  height,2/3 * _min,outline=c,width=w)
    self.create_line(x+width-2*_min/3 , y +  height, x , y + height ,x,y,width =w,fill=c)
def _createRectUL(self,x,y,width, height,c , w=w) :
    _min= min(width,height)
    
    self.create_line(x+ 2*_min /3 ,y, x+width , y, x +width , y+ height, x , y + height, x , y +height - _min * 1 / 3, width =w,fill=c)
    #canvas.create_arc(x+width/3, y+height/3, width * 2 / 3, style="arc", outline=c, width=6, start=270, end=360)
    #self.create_arc(x-width/3, y-height/3 , x+width , y +  height,start=270,extent = 90 , style="arc", outline=c, width=w) #,x+width, y+ height/3, 
    
    self.create_circle_arcUL( x , y +height - _min * 1 / 3,2/3 * _min,outline=c,width=w)
    
def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x-r, y-r, x+r, y+r **kwargs)    
def _create_circle_arcDR(self, x, y, r, **kwargs):    
    kwargs["extent"] = 90
    return self.create_arc(x-r, y-2*r, x+r, y, start = 270,  style="arc", **kwargs)
def _create_circle_arcUL(self, x, y, r, **kwargs):

    kwargs["extent"] = 90 #kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x, y-r, x+2*r, y+r, start = 90, style="arc", **kwargs)
  
def _createRect2(self,x,y,c,originX = originX,originY = originY,anzIn = 1, anzOut = 1) :
    wx = (maxX - x) * w
    k = 0
    wy = (maxY - y) * w
    if anzIn == 2 and anzOut == 1 :
            f = self.createRectUL
    elif anzIn == 1 and anzOut == 2  :
            f = self.createRectDR
    else :
            f = self.createRect
    f(originX + x * (stdWidth / 2 ) -  w / 2 * (x +y),
               originY + y * (stdHeight / 2) -  w / 2* (x + y),
               stdWidth +  w  * (x +y)  ,stdHeight +  w  * (x +y),c,wx + wy)
tkr.Canvas.create_circle_arc = _create_circle_arc
tkr.Canvas.create_circle_arcDR = _create_circle_arcDR
tkr.Canvas.create_circle_arcUL = _create_circle_arcUL
tkr.Canvas.createRectUL = _createRectUL 

tkr.Canvas.createRect = _createRect
tkr.Canvas.createRect2 = _createRect2
tkr.Canvas.createRectDR = _createRectDR
"""
canvas.createRectDR(50,50,200,100,"blue")
canvas.createRectUL(50,250,200,100,"blue")
canvas.createRect(originX + x * (stdWidth / 2 + 0.5*w) -  w * y, 
               originY + y * (stdHeight / 2 + 0.5*w) - w * x,
               stdWidth + 2 * w * y , stdHeight + 2 * w * x,c)

"""


#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)

#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)

#canvas.create_circle(150, 40, 20, fill="#BBB", outline="")




#canvas.createRect(50,50,100,200,'green',w=50)

#createRect(250,50 + (- 50 + 20)/2,100 ,200,'green',w=20)

canvas.createRect2(0,0,'green',anzOut=2)
canvas.createRect2(0,1,'blue')
canvas.createRect2(1,0,'purple',anzOut=2)
canvas.createRect2(1,1,'red',anzIn=2)
canvas.createRect2(2,0,'cyan',anzOut=2)
canvas.createRect2(2,1,'yellow',anzIn=2)
canvas.createRect2(3,0,'black')
canvas.createRect2(3,1,'white',anzIn=2)

#createRectDR(100,100, 300,300,'green')
#createRectUL(250,250, 300,300,'pink')


tkr.mainloop()