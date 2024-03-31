from Atom import *
import Area
from Particle import *
from State import *

class Molecule :
    def __init__ (self , _wld, _state,_goalState) :
        self.state = _state
        self.wld = _wld
        self.SP = Particle(_wld,_state.subobject,Sub,_goalState)
        self.UP = Particle(_wld,_state.uncertainty,Unc,_goalState)
    def move(self,forward,d) : #todo

        self.SP.move(forward,d)
        # think of erasing subobjects if uncertainty is full
        self.updateUncFromSubObj()
        self.draw()
    def room(self) :
        return self.SP.atom.room
    def getCanvas(self) :
        return self.wld.canvas
    
  
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
    