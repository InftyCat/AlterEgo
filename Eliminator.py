import Particle
import Atom
from BasicFunctions import Genus
#import State

"""

Definition. An eliminator is a pair target state T x (S x (S <= T) -> [(State , GoalState)])
Definition. There is a subquot |u| determined by a uncertainty u
Definition. The uncertainty ?s determined by a subquot s of $a$ is the maximal u such that s \ u = s.
    If it does not exist, we set it to infty.
Ex :
    - a goal state, it sends every S with S <= T to the empty List.
	- a frozen atom (A , goalstate): Given (s , u), then depending on the genus of A:
				uncertainty:
                    T = Full a (vorher infty )
                    Send to [(s , A) ,(|u| , A)]
                subquot:
                    T = Full a
                    Send to [((A,u) --> (A,?s)), (A,s) --> goalstate]




"""
 
class Eliminator :
    def __init__ (self,_targetState , _f) :
        self.targetState = _targetState
        self.f = _f
    def elim(self , s) :
    #    print("state now" , s)
        if (self.targetState.isBiggerThan(s)) : 
            return self.f(s) 
        else :
            print("goal state is not bigger than s!" )
            return None #[(s , self.targetState)]
def elimFromGoalState(goalstate) :
    return Eliminator(goalstate , lambda s : [])
def elimFromFrozenAtom(particle) :
    full = Atom.FullOrZeroAtom(particle.getRoom(),Atom.Full)
    if particle.genus == Genus.Unc :
            return Eliminator(full,lambda s : [((s.subobject.atom , particle.atom ) , s.goalstate) , ((s.uncertainty.atom , particle.atom), s.goalstate)])
    elif particle.genus == Genus.Sub :
         def f (s) :
              if s.subobject.atom.isKernel() :
                  return [((particle.atom , s.subobject.atom ) , s.goalstate) , ((particle.atom , s.uncertainty.atom ), (particle.atom , s.subobject.atom ))]
         return Eliminator(full ,f )
    return
