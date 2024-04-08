import Particle
import Atom
from State import *
from BasicFunctions import Genus , e
#import State


 
class Eliminator :
    def __init__ (self,_targetState : State , _f, _frozenParticle = None) : 
        e(_targetState,State)       

        self.targetState = _targetState
        self.f = _f
        self.frozenParticle = _frozenParticle
    def elim(self , s : State) :
    #    print("state now" , s)
        print("try to eliminate")
        if (not isinstance(self.targetState,State)) : 
             print("typecheck fail")
             return None
        if (self.targetState.isBiggerThan(s)) : 
            if (self.frozenParticle != None) : 
                 print("Erasing segments of frozen particle")
                 self.frozenParticle.area.eraseSegments()
            return self.f(s) 
        else :
            print("goal state is not bigger than s!" )
            return None #[(s , self.targetState)]

def elimFromGoalState(goalstate) :
    e(goalstate , State)
    return Eliminator(goalstate , lambda s : [])
def elimFromFrozenAtom(particle) :
    e(particle,Particle.Particle)
    full = Atom.FullOrZeroAtom(particle.getRoom(),Atom.Full)
    wld = particle.wld
    gs = particle.goalstate
    patom = particle.atom
    
    if particle.genus == Genus.Unc :
            compmaxState = State(wld , full , genFullUnc(particle.getRoom()) )
            def st(sa , ua) : 
                 return State(wld , sa,ua)
            f = lambda s : [( st(s.subobject , patom ) , gs) , (st(s.uncertainty , particle.atom), gs)]
            return Eliminator(compmaxState , f,particle)
    elif particle.genus == Genus.Sub :
         def f (s) :
              if s.subobject.atom.isKernel() :
                  return [st ((patom , s.subobject ) , gs) , (st (patom , s.uncertainty ), (patom , s.subobject ))]
         return Eliminator(full ,f ,particle)
    return
