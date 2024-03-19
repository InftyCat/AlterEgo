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
    
stdWidth = 600
stdHeight = 400
originX = 100
originY = 100
maxX = 4
maxY = 1
roundcoef = 1/2
rinv = 1 - roundcoef
# ALWAYS GO clockwise around the area!
class Segment :
    def __init__ (self,_canvas,_x1,_y1,_x2,_y2,_style,_w,_c,_dir):
        self.x1 = _x1
        self.x2 = _x2
        self.y2 =_y2
        self.y1 = _y1
        self.style = _style
        self.canvas = _canvas
        self.w = _w
        self.c = _c
        self.dir = _dir
    def draw(self) :
        if self.style == "line" :
            canvas.create_line(self.x1,self.y1,self.x2,self.y2,width = self.w,fill=self.c)
        else:
            a = whichArcPos(self.style, self.x1 , self.y1, self.x2,self.y2)
            
            if (not a == "") :
                r = abs(self.x1-self.x2)
                if (self.style == "DR"):
                    if a == "SO":
                        canvas.create_circle_arcDR(self.x2,self.y2,r,outline=self.c,width=self.w)        
                    if a == "NW":
                        canvas.create_circle_arcDR(self.x1,self.y1,r,outline=self.c,width=self.w)        
                else :
                    if a == "NW":
                        canvas.create_circle_arcUL(self.x1,self.y1,r,outline=self.c,width=self.w)        
                    if a == "NO":
                        canvas.create_circle_arcUL(self.x2,self.y2,r,outline=self.c,width=self.w)        
            else: 
                    print("radius mismatch!")
def whichArcPos(style,x1,y1,x2,y2) : 
   r = x2 - x1
   r2 = y2 - y1
   
   if (abs(r) == abs(r2)) :     
       if (r > 0 and style == "UL") : return "NW"
       if (r < 0 and style == "DR" ) : return "SO"
       if (r < 0 and style =="UL") : return "NO"
       if (r > 0 and style == "DR") : return "SW"

              
   else:
        print("this is not an arc")
        return ""
def HoriVertiArc (style,x1,y1,x2,y2):
    if style == "line":
        if (y1 == y2) : return "H"
        if (x1 == x2) : return "V"
    else:
        return whichArcPos(style,x1,y1,x2,y2)
def get_indices(lst, x):
    return [i for i, element in enumerate(lst) if element == x]
    
class Area : 
     def __init__ (self,_canvas,_c,_w)  :
         self.canvas = _canvas
         self.w = _w
         self.c = _c
         self.segments = []
     def create_segments (self,style, *kwargs):
        #print(kwargs,len(kwargs))
        segs = [[kwargs[i], kwargs[i+1],kwargs[i+2],kwargs[i+3]] for i in range(0, len(kwargs)-2, 2)]
        #directs = ["N"]
        ud = "N"
        lr = "W"
        direct = [HoriVertiArc(style,*p) for p in segs]
        nh = get_indices(direct, "H")
        nV = get_indices(direct, "V")
        hlab = [["N","S"],["NW,NO","SO","SW"],["NW,N,NO","SO","S","SW"]]
        vlab = [["O","W"],["ON,OS","WS","WN"],["ON,O,OS","WS","W","WN"]]
        nhp = int(len(nh) / 2) - 1
        nVp = int(len(nV) / 2) - 1
        
        for i in range (len(nh)):
            
            direct[nh[i]] = hlab[nhp][i]
        for i in range (len(nV)):
            direct[nV[i]] = vlab[nVp][i]
                
        for i in range(len(segs)) :
            #print("start",i)
            
            self.segments.append(Segment(self.canvas,*segs[i],_style=style,_w = self.w,_c = self.c,_dir = direct[i]) )
        
     def drawSegments (self):
        for seg in self.segments :
            seg.draw()
        
                        
def _createRectDR(self,x,y,width, height,c , w=w) :
    _min= min(width,height)
    a= Area(self,_c=c,_w=w)
    a.create_segments("line", x,y, x+width , y ,x+width, y+ _min*roundcoef)
    a.create_segments("DR", x+width, y+ _min*roundcoef,x+ width-(rinv) * _min , y +  height)
    #a.create_segments(False, x+ width-(rinv) * _min , y +  height,rinv * _min)
    a.create_segments("line",x+width-rinv * _min , y +  height, x , y + height ,x,y)
    a.drawSegments()
    return a
    #canvas.create_arc(x+width/3, y+height/3, width * 2 / 3, style="arc", outline=c, width=6, start=270, end=360)
    #self.create_arc(x-width/3, y-height/3 , x+width , y +  height,start=270,extent = 90 , style="arc", outline=c, width=w) #,x+width, y+ height/3, 
    
    #self.create_circle_arcDR(,outline=c,width=w)
    """ if (x2 - x1 == y2 - y1) : 
                if (x2 > x1):
                    
                    self.create_segments("line",x1,y1,x1 , y2 , x2 , y2)
                else :"""
                    
                    
def _createArc(self,x1,y1,x2,y2,style) :     
   if style == "line":
        if (x1 == x2 or y1 == y2):
            self.create_segments("line",x1,y1,x2,y2) # todo
        else:
            self.create_segments("line",x1,y1,x1 , y2 , x2 , y2)
   else:     
    if style == "DR" : 
        vorz = -1
    else :
        vorz = 1
    
    if (x1 == x2):
            r = y2 - y1
            self.create_segments("line",x1,y1,x1 + r,y1)
            if style == "DR" :
                
                self.create_segments(style,x1,y1 + vorz *r,x1 + r,y1)
            else :
                self.create_segments(style,x1 + r,y1,x1,y1 + vorz *r)
    else :
            if (x1 > x2) :
                self.create_segments("DR",x1,y1,x2,y2)
            else:
                self.create_segments("UL",x1,y1,x2,y2)
    
def _createArea(self,x,y,width,height,c,w,*arcs):

    _min= min(width,height)
    a= Area(self,_c=c,_w=w)
    a.create_segments("line",    x+ width - roundcoef*_min ,y, x+width , y)
    st = "line"
    if ("NO" in arcs) :
        st = "UL"
    a.createArc(x + width , y , x + width , y + _min * roundcoef,st)
    
    a.create_segments("line",x + width , y + _min * roundcoef , x + width , y + height - _min * roundcoef)
    if ("SO" in arcs) :
        st = "DR"
    else : 
        st = "line"
    a.createArc(x + width , y + height - _min * roundcoef , x +width - _min * roundcoef , y+ height,st)
    a.create_segments("line",x +width - _min * roundcoef , y+ height, x + _min * roundcoef , y+ height,x,y+height)
    if ("SW" in arcs) : 
        st = "DR" 
    else :
        st = "line"
    a.createArc(x  , y+ height , x , y + height - _min * roundcoef,st)
    a.create_segments("line",x , y +height - _min * roundcoef, x ,y + _min * roundcoef)
    if ("NW" in arcs):
        print("jop")
        st = "UL"
    else:
        st = "line"
    
    a.createArc( x ,y + _min * roundcoef,x + _min * roundcoef,y,st)
    a.create_segments("line",x + _min * roundcoef,y,x + width - _min*roundcoef,y)
    a.drawSegments()
    return a                    
            
            
def _createRectUL(self,x,y,width, height,c , w) :
    _min= min(width,height)
    a= Area(self,_c=c,_w=w)
    a.create_segments("line",    x+ rinv*_min ,y, x+width , y, x +width , y+ height, x , y + height, x , y +height - _min * roundcoef)    
    a.create_segments("UL", x , y +height - _min * roundcoef, x+ rinv*_min ,y)
    a.drawSegments()
    return a

    
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
  
def _createRect2(self,x,y,c,originX = originX,originY = originY,anzIn = 1, anzOut = 1,dl = False, ur = False) :
    wx = (maxX - x) * w 
    k = 0
    wy = (maxY - y) * w 
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
    self.createArea(originX + x * (stdWidth / 2 ) -  w / 2 * (x +y),
               originY + y * (stdHeight / 2) -  w / 2* (x + y),
               stdWidth +  w  * (x +y)  ,stdHeight +  w  * (x +y),c,wx + wy,*st)
tkr.Canvas.create_circle_arc = _create_circle_arc
tkr.Canvas.create_circle_arcDR = _create_circle_arcDR
tkr.Canvas.create_circle_arcUL = _create_circle_arcUL
tkr.Canvas.createRectUL = _createRectUL 
tkr.Canvas.createArea = _createArea
Area.createArc = _createArc
tkr.Canvas.createRect = _createRect
tkr.Canvas.createRect2 = _createRect2
tkr.Canvas.createRectDR = _createRectDR




canvas.createRect2(0,0,'green',anzOut=2)
canvas.createRect2(0,1,'blue',ur=True)
canvas.createRect2(1,0,'purple',anzOut=2)
canvas.createRect2(1,1,'red',anzIn=2,ur=True)
canvas.createRect2(2,0,'cyan',anzOut=2,dl=True)
canvas.createRect2(2,1,'yellow',anzIn=2)
canvas.createRect2(3,0,'black',dl=True)
canvas.createRect2(3,1,'white',anzIn=2)


tkr.mainloop()
"""
canvas.createRectDR(50,50,200,100,"blue")
canvas.createRectUL(50,250,200,100,"blue")
canvas.createRect(originX + x * (stdWidth / 2 + 0.5*w) -  w * y, 
               originY + y * (stdHeight / 2 + 0.5*w) - w * x,
               stdWidth + 2 * w * y , stdHeight + 2 * w * x,c)

"""

"""



#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)

#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)

#canvas.create_circle(150, 40, 20, fill="#BBB", outline="")




#canvas.createRect(50,50,100,200,'green',w=50)

#createRect(250,50 + (- 50 + 20)/2,100 ,200,'green',w=20)
#createRectDR(100,100, 300,300,'green')
#createRectUL(250,250, 300,300,'pink')


"""