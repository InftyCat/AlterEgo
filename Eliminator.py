class Eliminator :
    def __init__ (_target , _f) :
        self.target = _target
        self.f = _f
    def elim(self , s) :
        if (self.target.isBiggerThan(s)) : 
            return self.f(s) 
        else :
            print("goal state is not bigger than s!" )
            return s
def elimFromGoalState(goalstate) :
    self.target = goalstate
    self.f = lambda s : []
def elimFromFrozenAtom(particle) :
    return
