import Room
from Atom import *
from State import *
import Area
import Molecule
from Eliminator import *
import Moving
from BasicFunctions import Genus, e
#from Area import *



def swapGenus(genus: Genus) -> Genus :
    if genus == Genus.Sub :
        return Genus.Unc
    elif genus == Genus.Unc :
        return Genus.Sub

class Particle :
    def __init__ (self , _molecule , _atom , _genus , _goalstate = None,) : # , coparticle = None ) :
        self.atom = _atom
        self.genus = _genus
        self.goalstate = _goalstate
        self.frozen = False
        self.wld = _molecule.wld
        self.history = []
        e(_molecule, Molecule.Molecule)
        self.molecule = _molecule
        self.area = None #self.initArea()
        
        #print("I was born as particle " + str(id(self)))
        #self.coparticle= 
        
            
        
    def generateMoleculeFromSub(self,eliminator) :
        _state = self.wld.canState(self.atom)    
        self.molecule = self.wld.canMolecule2(lambda x : self , _state.uncertainty,eliminator)
        self.wld.molecules.append(self.molecule)
        self.molecule.UP.initArea()
        #self.molecule.initState()
        self.molecule.jumpable = True
        
    def activateTimejump(self) :
         if (not self.molecule.jumpable) :                     
               oldcoparticle = self.getCoParticle()
               #self.history.append(self.atom)
               eliminator = oldcoparticle.freeze()
               eliminator.setNewHistory(self.history + [self.atom],oldcoparticle.history)
               self.genus = Genus.Sub
               print("freezing complete , adding molecule")
               self.generateMoleculeFromSub(eliminator) 
               print(self.genus , " now jumpable!") # with history ") # , self.history)               
         else :
             print("sth fishy")
    
    
    def printHistory(self) : 
        s = ""
        for a in self.history : 
            s += str(a) + ","
        return s
    def jumpback(self) :
        if (len(self.history)==0) : 
            print(self , " : I have no history!")
        else :
            h = self.history[-1]
            self.history = self.history [:-1]
            self.updateAtom(h,jumpback=True)
            #self.draw


    def __str__(self) :
        return str(self.atom) #+ "_Id : " + str(id(self) ) #str(self.genus) + "__" +  #  "_Age : " + str(len(self.history))
    def move(self,forward, d) :
        mvg = Moving.Moving(self.wld,self)
        if forward :
           #if 
          r = mvg.forward(d)
        else :
           r = mvg.backward(d)
        return r
    def getCoParticle(self) : 
         cogenus = swapGenus(self.genus)
         return self.molecule.getParticleFromGenus(cogenus)
    def uncWedge(self,r) :
        ur = self.getUncCoRoom()
        ur.wedge(self.wld,r)
        
        if not ur.infty :
#            self.updateSubob
            self.updateAtom(self.wld.genUnc(r, ur.room)) # return newState(self,subobject,uncRoom) # self.updateState(newState(self,subobject,uncRoom))
        else :
            #print("unc wedge infty",self.atom)
            self.updateAtom(genFullUnc(r)) # self.updateState(State(self,))"""
    def erase(self) : 
        if self.area != None :
            self.area.eraseSegments()
    def updateAtom(self,_atom : Atom,jumpback=False) :
        
        if (not jumpback) : 
            self.history.append(self.atom)

        self.erase()
        self.atom = _atom 

    def getRoom(self) :
        return self.atom.room
    def initArea(self) :      
            self.area = self.getArea()
            if self.genus == Genus.Sub :
                self.area.filled = True#
                #leave it as it is otherwise
                #= self.genus == Genus.Sub
            #print("inited area" , self.area == None)
    def getGoalState(self) :
        """if (self.goalstate == None) :
            if (self.genus == Genus.Unc) : 
                print("I am an uncertainty particle, i dont know the goalstate!")
                
        else :"""
        return self.goalstate
    def freeze (self ) :
        #todo
        self.frozen = True
        self.wld.molecules.remove(self.molecule)
        
        el = FrozenAtomEliminator(self)
        self.molecule = None
        """if (el != None) : 
            print("constructed eliminator")
        else :
            print("sth went wrong")"""
        print("Now frozen: ", self)
        return el

    def getUncCoRoom(self) : 
        return self.atom.getKernelRoom(self.genus == Genus.Unc)
    
    def getArea(self) : 
        
        atom = self.atom
        if self.genus == Genus.Sub :
        #atom = self.subobject()
            return atom.getArea(self.wld)
        elif  self.genus == Genus.Unc :
                   
        #atom = self.uncertainty()
            (x1,y1) = atom.room
            r = self.getUncCoRoom()
            if r.infty == False :
                (x2,y2) = r.room
                #print("updated uncarea")
                return self.wld.createker(x1,y1,x2,y2,unc=True)
            else :
                
                #print("uncarea now infty")
                print("also this code")
                a = self.wld.areas[(x1,y1)]
                full = Area.Area(self.wld.canvas,"#000000",a.w * 2,a.width,a.height,_filled=True)
                for s in self.wld.areas[(x1,y1)].segments : full.stealSegment(s)
                return full
        