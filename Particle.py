import Room
from Atom import *
from State import *
import Area
import Molecule
import Eliminator
import Moving
from BasicFunctions import Genus
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
        self.area = None
        self.wld = _molecule.wld
        self.history = []
        self.molecule = _molecule
        #self.coparticle= 
        
            
        
    def generateMoleculeFromSub(self,eliminator) :
        _state = self.wld.canState(self.atom)    
        self.molecule = self.wld.canMolecule(_state,eliminator)
        self.molecule.jumpable = True
        
    def activateTimejump(self) :
         if (not self.molecule.jumpable) :
              
         
               oldcoparticle = self.getCoParticle()
               eliminator = oldcoparticle.freeze()
               self.generateMoleculeFromSub(eliminator) 

            

               print("now jumpable!")
            

    
    def __str__(self) :
        return str(self.atom)
    def move(self,forward, d) :
        mvg = Moving.Moving(self.wld,self)
        if forward :
           #if 
          mvg.forward(d)
        else :
           mvg.backward(d)
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

    def updateAtom(self,_atom) :
        self.history.append(self.atom)
        self.area.eraseSegments()
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
        self.frozen = True
        self.molecule = [] 
        
        return Eliminator.elimFromFrozenAtom(self)

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
        