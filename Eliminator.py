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
    def elim(self , s : State , wld) :
    #    print("state now" , s)
        #("try to eliminate")
        e(s , State)
        if (not isinstance(self.targetState,State)) : 
             print("typecheck fail")
             return None
        if (self.targetState.isBiggerThan(wld, s)) : 
            if (isinstance(self,FrozenAtomEliminator)) :
                if (self.frozenParticle != None) : 
                    print("Erasing segments of frozen particle")
                    self.frozenParticle.erase()
            return self.f(s) 
        else :
            
            print("goal state is not bigger than s!" )
            return None #[(s , self.targetState)]

class GoalStateEliminator(Eliminator): 
    def __init__(self , _targetState) : 
     self.goalState = _targetState
     super().__init__(_targetState , lambda s : [])
    def __str__(self) :
        return "[->"  + str(self.goalState) + "]" 
    def __eq__(self,other) : 
         return self.goalState == other.goalState
    def getNewHistory(self,gen : Genus) : 
         return []
"""def elimFromGoalState(goalstate) :
    e(goalstate , State)
    return Eliminator(goalstate , lambda s : [])"""

class FrozenAtomEliminator(Eliminator) : 
    def __eq__(self,other) : 
         return self.frozenParticle == other.frozenParticle
    def __str__(self) : 
         return "[°-> " + str(self.frozenParticle) + "]"
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

        compmaxState = State(wld , full , genFullUnc(particle.getRoom()) )
        if particle.genus == Genus.Unc :
                
                f = lambda s : [( st(s.subobject , patom ) , elim) , (st(s.uncertainty , particle.atom), elim)]
                super().__init__(compmaxState , f)
        elif particle.genus == Genus.Sub :
            def f (s : State) :
                print("try to eliminate." , s , wld)
                if s.subobject.isKernel(wld) :
                    ssub = s.subobject
                    ssub.info = Atom.Ker
                    return [(st (patom , ssub ) , elim) , (st (patom , s.uncertainty ), GoalStateEliminator (st (patom , ssub )))]
                else :
                    print("sorry you are not a kernel!")
            super().__init__(compmaxState ,f )
        return
    def setNewHistory(self,sh,uh) :
         self.newSubHistory = copy.deepcopy(sh )
         self.newUncHistory = copy.deepcopy(uh )
         print("new history of eliminator : " , sh , " _ " ,uh)
    def getNewHistory(self,gen : Genus) :
        if gen == Genus.Sub :
            return self.newSubHistory #frozenParticle.history
        else :
         return self.newUncHistory #frozenParticle.history