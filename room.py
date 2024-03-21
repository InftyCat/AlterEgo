#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:59:46 2024

@author: tim
"""

import tkinter as tkr
w =6
tk = tkr.Tk()
frame = tkr.Frame(tk)
frame.grid(row=0, column=0)
canvas = tkr.Canvas(frame, width=1000, height=700)
canvas.grid(row=0,column=0)



def _createRect(self,x,y,width,height,c,w=w) :
    self.create_rectangle(x,y,x+width,y+height,outline=c,width=w)
    
stdWidth = 300
stdHeight = 300
originX = 200
originY = 100
maxX = 4
maxY = 1
roundcoef = 1/2
rinv = 1 - roundcoef
#def _createObj(self):
    #self.obj =

# ALWAYS GO clockwise around the area!
def so(s):
    return sorted(list(s))
def strEq(str1,str2):
    return (sorted(list(str1)) == sorted(list(str2)))
class Segment :
    def __init__ (self,_canvas,_x1,_y1,_x2,_y2,_style,_w,_c):
        self.x1 = _x1
        self.x2 = _x2
        self.y2 =_y2
        self.y1 = _y1
        self.style = _style
        self.canvas = _canvas
        self.w = _w
        self.c = _c
        #self.dir = _dir
    def draw(self) :
        if self.style == "line" :
            #w = self.w
            canvas.create_line(self.x1,self.y1,self.x2,self.y2,width = self.w,fill=self.c)
        else:
            a = whichArcPos(self.style, self.x1 , self.y1, self.x2,self.y2)
            
            if (not a == "") :
                r = abs(self.x1-self.x2)
                if (self.style == "DR"):
                    if so(a) == so("SO"):
                        canvas.create_circle_arcDR(self.x2,self.y2,r,outline=self.c,width=self.w)        
                    if so(a) == so("SW"):
                        
                        canvas.create_circle_arcDR(self.x1,self.y1,r,outline=self.c,width=self.w)        
                else :
                    if so(a) == so("NW"):
                        canvas.create_circle_arcUL(self.x1,self.y1,r,outline=self.c,width=self.w)        
                    if so(a) == so("NO"):
                        canvas.create_circle_arcUL(self.x2,self.y2,r,outline=self.c,width=self.w)        
            else: 
                    print("radius mismatch!")
    def enlarge(self,x2n,y2n) :
        self.x2 = x2n
        self.y2 = y2n
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
def get_indices(lst, *x):
    return [i for i, element in enumerate(lst) if element in x]
    
class Area : 
     def __init__ (self,_canvas,_c,_w)  :
         self.canvas = _canvas
         self.w = _w
         self.c = _c
         self.segments = []
     def create_segments (self,style, *kwargs,glue=False):
        #print(kwargs,len(kwargs))
        segs = [[kwargs[i], kwargs[i+1],kwargs[i+2],kwargs[i+3]] for i in range(0, len(kwargs)-2, 2)]
        #directs = ["N"]
        
        for i in range(len(segs)) :
            #print("start",i)
            if (segs[i][0],segs[i][1]) != (segs[i][2],segs[i][3]) :
                if glue : 
                    self.segments[-1].enlarge(segs[i][2] , segs[i][3]) 
                else :
                    self.segments.append(Segment(self.canvas,*segs[i],_style=style,_w = self.w,_c = self.c)) #,_dir = direct[i]) )
     def generateDirections(self) :
        
        direct = [HoriVertiArc(p.style,p.x1,p.y1,p.x2,p.y2) for p in self.segments]
        print(direct)
        nh = get_indices(direct, "H","SO","NW")
        nV = get_indices(direct, "V","SO","NW","ON","WS")
        hlab = [["N","S"],["NO","SO","SW","NW"],["NO","SO","S","SW","NW","N"]]
        vlab = [["O","W"],["ON","OS","WS","WN"],["ON","O","OS","WS","W","WN"]] ## renamed OS to SO
        nhp = int(len(nh) / 2) -1
        nVp = int(len(nV) / 2)  - 1
        #nhp = max(nhp,nVp)
        #nVp = max(nhp,nVp)
        
        for i in range(len(hlab[nhp])):
            h = hlab[nhp][i]
            n = direct[nh[i]] 
            if n == "H" :
                direct[nh[i]] = h
            else :
                if (so(n) != so(h)) :
                    print(n,h,"something went wrong")
        for i in range(len(vlab[nVp])):
                h = vlab[nVp][i]
                n = direct[nV[i]] 
                if n == "V" :
                    direct[nV[i]] = h
                else :
                    if (so(n) != so(h)) :
                        print(n,h,"something went wrong")   
                """
                j = 0
                
                def cond (i,j , nhnv , arr) :
                    if (i + j < len(arr)) :
                b = False
                for k in range(len(self.segments)):
                    
                        p = self.segments[k]
                        d = direct [k]
                        if True : # d != arr[i+j]:    
                            if p.style != "line" and not isSpecialArc(p.style, p.x1, p.y1, p.x2, p.y2) and False :
                                if  so(arr[i+j]) == so (d) : 
                                    print(arr[i+j],d,"wichtig!")
                                    
                                b = b or so(arr[i+j]) == so (d)
                            else :
                                b = b or arr [i+j] == d
                return b
            else:
                return False
                
          
        for i in range (len(nh)):
            
            
            
                while cond(i,j,nh,hlab[nhp]) : 
                    
                    j = j + 1
                   
                    #print("inc",j,hlab[nhp][i+j])
                #print(nh[i],hlab[nhp][i+j])    
                if (i + j < len(hlab[nhp])) : direct[nh[i]] = hlab[nhp][i+j]
            
            
        j = 0            
        for i in range (len(nV)):
      
                while cond (i,j,nV, vlab[nVp]): 
                    print("inc",j,vlab[nVp][i+j])
                    j = j + 1
            
                    
                
                
                if (i+j < len(vlab[nVp])): 
                    print(nV[i],vlab[nVp][i+j])    
                    direct[nV[i]] = vlab[nVp][i+j]
            """
        return direct
     def drawPoints(self) : 
         for seg in self.segments :
             r = 10
             if (seg == self.segments[0]) :
                 r = 20
             self.canvas.create_circle_arc(seg.x1,seg.y1,r,start = 0,end = 359,fill="black")
     def drawSegments (self):
        for seg in self.segments :
            seg.draw()
                  
def isSpecialArc(style,x1,y1,x2,y2):
        return style != "line" and x1 == x2
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
    
    if (isSpecialArc(style,x1,y1,x2,y2)):
            r = y2 - y1
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
        
        st = "UL"
    else:
        st = "line"
    
    a.createArc( x ,y + _min * roundcoef,x + _min * roundcoef,y,st)
    a.create_segments("line",x + _min * roundcoef,y,x + width - _min*roundcoef,y)
    a.drawSegments()
    return a                    
            

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
    return self.create_arc(x-r, y-r, x+r, y+r , **kwargs)    
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
    return self.createArea(originX + x * (stdWidth / 2 ) -  w / 2 * (x +y),
               originY + y * (stdHeight / 2) -  w / 2* (x + y),
               stdWidth +  w  * (x +y)  ,stdHeight +  w  * (x +y),c,wx + wy,*st)

def _showImg(self,so,x1,y1,x2,y2):
    self.coords(so,x1,y1,x2,y2)
    #subobject = self.createRect(200,200,50,50,fill="purple")
tkr.Canvas.create_circle_arc = _create_circle_arc
tkr.Canvas.create_circle_arcDR = _create_circle_arcDR
tkr.Canvas.create_circle_arcUL = _create_circle_arcUL
tkr.Canvas.showImg = _showImg
tkr.Canvas.createArea = _createArea
Area.createArc = _createArc
tkr.Canvas.createRect = _createRect
tkr.Canvas.createRect2 = _createRect2




a00 = canvas.createRect2(0,0,'green' ,anzOut=2)#  ,ur=True,dl=True)
#a = canvas.createRect2(0,2,'green')
#a.drawPoints()

a01 = canvas.createRect2(0,1,'blue',ur=True)
a10 = canvas.createRect2(1,0,'purple',anzOut=2)
a11 = canvas.createRect2(1,1,'red',anzIn=2,ur=True)
#obj = canvas.create
#canvas.createRect2(2,0,'cyan',anzOut=2,dl=True)
#canvas.createRect2(2,1,'yellow',anzIn=2)

#canvas.createRect2(3,0,'black',dl=True)
#canvas.createRect2(3,1,'white',anzIn=2)

#print(a.generateDirections())
subobject =   canvas.create_rectangle(originX,originY,450,450,fill="purple")
but = tkr.Button(frame, text="test", command=canvas.showImg(subobject,0,0,0,0))
#but.pack()
but.grid(row=1,column=0)
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