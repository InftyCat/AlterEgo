import Particle
import Atom
from State import *
import copy
from BasicFunctions import Genus , e
#import State

 
class Eliminator :
    def __init__ (self,_targetState : State , _f) : 
        e(_targetState,State)       

        self.targetState = _targetState
        self.f = _f
        #self.frozenParticle = _frozenParticle
        #self.goalState = _
    def elim(self , s : State) :
    #    print("state now" , s)
        #("try to eliminate")
        if (not isinstance(self.targetState,State)) : 
             print("typecheck fail")
             return None
        if (self.targetState.isBiggerThan(s)) : 
            if (isinstance(self,FrozenAtomEliminator)) :
                if (self.frozenParticle != None) : 
                    print("Erasing segments of frozen particle")
                    self.frozenParticle.erase()
            return self.f(s) 
        else :
            
            #print("goal state is not bigger than s!" )
            return None #[(s , self.targetState)]

class GoalStateEliminator(Eliminator): 
    def __init__(self , _targetState) : 
     self.goalState = _targetState
     super().__init__(_targetState , lambda s : [])
    def __eq__(self,other) : 
         return self.goalState == other.goalState
    def getNewHistory(self) : 
         return []
"""def elimFromGoalState(goalstate) :
    e(goalstate , State)
    return Eliminator(goalstate , lambda s : [])"""

class FrozenAtomEliminator(Eliminator) : 
    def __eq__(self,other) : 
         return self.frozenParticle == other.frozenParticle
    def __init__(self  ,  particle) : 
        self.frozenParticle = particle
        self.newHistory = []

        e(particle,Particle.Particle)
        full = Atom.FullOrZeroAtom(particle.getRoom(),Atom.Full)
        wld = particle.wld
        elim = particle.molecule.eliminator
        e(elim, Eliminator)
        patom = particle.atom
        def st(sa , ua) : 
                    return State(wld , sa,ua)

        if particle.genus == Genus.Unc :
                compmaxState = State(wld , full , genFullUnc(particle.getRoom()) )
                
                f = lambda s : [( st(s.subobject , patom ) , elim) , (st(s.uncertainty , particle.atom), elim)]
                super().__init__(compmaxState , f)
        elif particle.genus == Genus.Sub :
            def f (s : State) :
                if s.subobject.atom.isKernel() :
                    return [st ((patom , s.subobject ) , elim) , (st (patom , s.uncertainty ), GoalStateEliminator (st (patom , s.subobject )))]
            super().__init__(full ,f )
        return
    def setNewHistory(self,nh) :
         self.newHistory = copy.deepcopy(nh )
         print("new history of eliminator : " , nh)
    def getNewHistory(self) :
         return self.newHistory #frozenParticle.history