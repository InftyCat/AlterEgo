from Atom import *
import Area
import Particle #Genus, Particle
from State import *
from BasicFunctions import Genus
    #uncState = self.wld.canState(self.atom)    

    
        
class Molecule :
    def __init__ (self, _wld ,_eliminator, initSP , initUP) :             
        self.wld = _wld
        self.SP = initSP(self)
        self.UP = initUP(self)
        self.focus = Genus.Sub
        self.jumpable = False
        self.state = State(_wld,self.SP.atom,self.UP.atom)
   
    def swapFocus(self) :
        self.focus = Particle.swapGenus(self.focus)
    def getParticleFromGenus(self,genus) :
        if genus == Genus.Sub :
            return self.SP
        else :
            return self.UP
    def jumpback(self) : 
        if (self.jumpable) : 
            return
        else :            
            self.getParticleFromGenus(self.focus).activateTimejump()
    def move(self,forward,d) : #todo

        self.SP.move(forward,d)
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
            self.wld.molecules = self.wld.molecules[0:-2] +  newM
        
        print("eliminated molecule. Remaining : " , len(self.wld.molecules))
        self.erase()
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
    def updateStateFromSubobj(self,subobject) :
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
    