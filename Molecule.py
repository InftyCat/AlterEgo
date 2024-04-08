from Atom import *
import Area
import Particle #Genus, Particle
from State import *
import World
from Eliminator import *
from BasicFunctions import Genus , e
    #uncState = self.wld.canState(self.atom)    

    
        
class Molecule :
    def __init__ (self, _wld : World ,_eliminator, initSP , initUP) :             
        self.wld = _wld
        self.SP = initSP(self)
        self.UP = initUP(self)
        self.focus = Genus.Sub
        self.jumpable = False
        self.state = State(_wld,self.SP.atom,self.UP.atom)
        self.eliminator = _eliminator
    def __str__(self) : 
        return str(self.SP) + "," + str (self.UP)
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
                print("History is empty! This should not happen")
            else :
                #print(self.SP.history)
                self.SP.jumpback()
                if len(self.subobject().history) == 0 :
                    self.jumpable = False
                

            
            self.updateUncFromSubObj()
            self.draw()
            
        else :           
            p =  self.getParticleFromGenus(self.focus)
         
            eliminator = p.activateTimejump()

    def move(self,forward,d) : #todo
        self.jumpable = False
        hasMoved = self.SP.move(forward,d)
        if hasMoved :
        # think of erasing subobjects if uncertainty is full
            self.updateUncFromSubObj()
            self.draw()
    def room(self) :
        return self.SP.atom.room
    def getCanvas(self) :
        return self.wld.canvas
    def getState(self) :
        return State(self.wld,self.subobject().atom , self.uncertainty().atom)
    def fin(self) :
        newM = self.eliminator.elim(self.getState())
        if newM == None : 
            print("Not finishable!")
        else :
            self.wld.molecules = self.wld.molecules[0:-2] 
            self.erase()
            for m in newM :
                (s , gs) = m

                e(s , State)
                e(gs , State)
                m = self.wld.canMolecule(s,elimFromGoalState(gs))
                self.wld.molecules.append(m)
                m.draw()
               
        anz =  len(self.wld.molecules)
        print("eliminated molecule. Remaining : " ,anz)
        if (anz > 0) :
            print("next molecule:" , self.wld.mm())
        else : 
            print("You won!")
    
    def draw(self) :
        
        self.subobject().initArea()
        self.uncertainty().initArea()
       # print(self.subobject().area)
        self.drawAtom()
        self.uncertainty().area.drawSegments() #Todo
    def update(self,state) :    
      #self.deleteState()
      self.state = state
      #print("State  is now" , state)
      self.SP.updateAtom(state.subobject)
      self.UP.updateAtom(state.uncertainty)
      self.draw()
    #def update(self,subobj) :
    def updateUncFromSubObj(self) :
        
        self.uncertainty().uncWedge(self.subobject().getRoom())
    def erase(self) :
        self.SP.area.eraseSegments()
        self.UP.area.eraseSegments() 
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
    

    def drawAtom(self) :
        self.subobject().area.drawSegments() 
        self.subobject().area.drawMiddlepoint()
    