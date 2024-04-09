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
               eliminator.setNewHistory(self.history + [self.atom])
               print("freezing complete , adding molecule")
               self.generateMoleculeFromSub(eliminator) 
               print("now jumpable!") # with history ") # , self.history)               
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
        ur.wedge(r)
        
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
            self.area = self.getAreaFromAtom()
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
        
    def getAreaFromAtom(self) : 
        
        atom = self.atom
        if self.genus == Genus.Sub :
        #atom = self.subobject()
            (x1,y1) = atom.room
            
            (x2,y2) = atom.getCoRoom()
            #print(".",atom,(x1,y1),(x2,y2))
            #print(x1,y1,x2,y2)
            if atom.info == Ker :     
                return self.wld.createker(x1,y1,x2,y2)
            elif atom.info == Im :
                return self.wld.createImg(x1,y1,x2,y2)
            elif atom.info == Full :
                full = Area.Area(self.wld.canvas,self.wld.areas[(x1,y1)].c,15)
                for s in self.wld.areas[(x1,y1)].segments : full.stealSegment(s)
                return full
            elif atom.info == Atom.Zero:
                zero = Area.Area(self.wld.canvas,"black",3)
                for s in self.wld.areas[(x1,y1)].segments : zero.stealSegment(s)
                return zero
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
                a = self.wld.areas[(x1,y1)]
                full = Area.Area(self.wld.canvas,"black",a.w * 2)
                for s in a.segments : full.stealSegment(s)
                return full
        