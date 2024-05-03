import Atom
class MovingUnc :
    def __init__(self,_tk,canvas,_wld) :
            self.tk = _tk
            self.wld = _wld
            self.uncpnt = {}
            self.canvas = canvas
            
#self
    
    def uncAction(self) :
     for m in self.wld.molecules :
        unc = m.uncertainty()
        if (not unc.frozen) : 
            if (unc in self.uncpnt.keys()) : 
                    self.canvas.delete(self.uncpnt[unc])
            if (unc.atom.info != Atom.Zero) :
            # print("uncAction", unc)
                p = unc.atom.getArea(self.wld).random_Point_in_Polygon()

                (x,y) = (p.x,p.y)
                
                self.uncpnt[unc] =self.canvas.create_circle_arc(x,y,10,start = 0,end = 359,fill=self.wld.mm().subobject().area.c)
                
    #print(wld.mm().room())
    def removePart(self,unc) :
        if (unc in self.uncpnt.keys()) : 
                    self.canvas.delete(self.uncpnt[unc])
        self.uncpnt.pop(unc)

    def repeat_every_second(self) : 
        
        self.uncAction()
        if (not self.wld.gameEnd()) : 
            self.tk.after(100,self.repeat_every_second)            