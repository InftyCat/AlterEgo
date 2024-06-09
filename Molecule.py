from Atom import *
import Area
import Particle #Genus, Particle
from State import *
import World

from Eliminator import *
from BasicFunctions import Genus , e , Helper
    #uncState = self.wld.canState(self.atom)    

    
        
class Molecule :
    def __init__ (self, _wld : World ,_eliminator, initSP , initUP) : #, initAreas = False) :             
        self.wld = _wld
        self.SP = initSP(self)
        self.UP = initUP(self)
        self.focus = Genus.Sub
        self.jumpable = False
        #self.state = State(_wld,self.SP.atom,self.UP.atom)
        self.eliminator = _eliminator
        #if (initAreas) :
         #   self.initState()
    def __str__(self) : 
        return str(self.getState()) #+ " , " +  str(self.eliminator) #) str(len(self.SP.history))
    def swapFocus(self) :
        self.focus = Particle.swapGenus(self.focus)

    def getParticleFromGenus(self,genus) :
        if genus == Genus.Sub :
            return self.SP
        else :
            return self.UP
        
    def jumpback(self) : 
        if (self.jumpable) : 
            #u = self.UP.atom
            if len(self.SP.history) == 0 :
                print("History is empty!") # This should not happen")
            else :
                #print(self.SP.history)
                self.SP.jumpback()
                if len(self.subobject().history) == 0 :
                    print("Because I have no history (anymore), I am not jumpable anymore")
                    self.jumpable = False
                

            
            self.updateUncFromSubObj()
            self.draw()
            
        else :           
            p =  self.getParticleFromGenus(self.focus)
            print("->",p.genus)
            eliminator = p.activateTimejump()
          

    def move(self,forward,d) : #todo
        self.jumpable = False
        self.focus = Genus.Sub
        

        hasMoved = self.SP.move(forward,d)
        while (not hasMoved) :
            print("rightbefore has moved" , self.subobject())
            self.assCnt = 0
            if not self.wld.refineMM(forward) : 
                print("refining stopped, breaking move...")
                break
            print("now its:" , self.subobject())
            hasMoved = self.SP.move(forward,d)
        if hasMoved :
        # think of erasing subobjects if uncertainty is full
            self.updateUncFromSubObj()
            self.wld.uncPart.removePart(self.subobject())
            self.wld.refineMM(True)
            self.draw()
    def room(self) :
        return self.SP.atom.room
    def getCanvas(self) :
        return self.wld.canvas
    def getState(self) :
        return State(self.wld,self.subobject().atom , self.uncertainty().atom)
    def checkFin(self) :
        if Helper.EliminateToOtherMolecules in self.wld.helper :
            for i in range (len(self.wld.molecules)) : 
                m = self.wld.molecules[i]
                if (m != self) :
                    if m.isBiggerThan(self) :
                        print("Eliminated to another molecule")
                        return []
                    #todo
        return self.eliminator.elim(self.getState(),self.wld)
    def getHistory(self) :
        sh = self.SP.history 
        uh = self.UP.history
        if len(sh) == len(uh) :
            l = len(self.SP.history)
            s = ""
            for i in range(l) :
                s += str(State(self.wld, sh[i] ,uh[i])) + " ; "
            return s
        else :
            return self.SP.printHistory() + " | " + self.UP.printHistory()
    
    def fin(self) :
        #check wether other molecules have bigger goals and equal eliminators
        newM = self.checkFin()
        #if newM == None : 
            #print("Not finishable!")
        if newM != None :  #else :
            self.wld.removeFromList(self) 
            self.wld.uncPart.removePart(self.uncertainty())
            self.erase()
            self.wld.canvas.update()
            for m in newM :
                (s , elim) = m

                e(s , State)
                e(elim , Eliminator)
                m = self.wld.canMolecule(s,elim)
                if (m != newM[-1]) : 
                    m.SP.history = self.eliminator.getNewHistory(Genus.Sub)
                    m.UP.history = self.eliminator.getNewHistory(Genus.Unc)
                    print("history of first molecule updated to " , m.getHistory())
                self.wld.molecules.append(m)
                m.draw()
               
            anz =  len(self.wld.molecules)
            print("eliminated molecule. Remaining : " ,anz)
            if (anz > 0) :
                print("next molecule:" , self.wld.mm())
            else : 
                print("You won!")
            self.wld.canvas.update()
    
    def draw(self) :
        
        self.subobject().initArea()
        self.uncertainty().initArea()
       # print(self.subobject().area)
        
        self.drawAtom()
        #print("UNC=",self.uncertainty())

        self.uncertainty().area.drawSegments()
    def update(self,state) :    
      #self.deleteState()
      #self.state = state
      #print("State  is now" , state)
      self.SP.updateAtom(state.subobject)
      self.UP.updateAtom(state.uncertainty)
      self.draw()
    #def update(self,subobj) :
    def updateUncFromSubObj(self) :
        
        self.uncertainty().uncWedge(self.subobject().getRoom())
    def erase(self) :
        self.SP.erase()
        self.UP.erase() 
        self.wld.canvas.update()
    def updateStateFromSubobj(self,subobject : Atom) :
        self.subobject().updateAtom(subobject)
        self.updateUncFromSubObj()

        self.draw()
        """r = self.uncertainty().getUncCoRoom()
        r.wedge(subobject.room)
        print(r)
        #print("uncRoom",uncRoom)
        uncRoom  = r.room
        if not r.infty :
#            self.updateSubob
            return newState(self,subobject,uncRoom) # self.updateState(newState(self,subobject,uncRoom))
        else :
            return State(self,subobject,genFullUnc(subobject)) # self.updateState(State(self,))"""

    def subobject (self) :
        return self.SP
    def initState(self) : 
        self.subobject().initArea()
        self.uncertainty().initArea()
    def uncertainty(self) :
        return self.UP #state.uncertainty            
    
    def isBiggerThan(self, other) :
        b1 = False
        if type(self.eliminator) == type(other.eliminator) : 
            b1 = self.eliminator == other.eliminator
        b2 = self.getState().isBiggerThan(self.wld, other.getState())
        ret = b1 and b2
        #print(self , " > " , other , " = " , b1 , " & " , b2 , " = " , ret)
        return b1 and b2
    def drawAtom(self) :        
        self.subobject().drawSegsandMp()
        
    