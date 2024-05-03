from Atom import Hori , Verti, Diag
from Morphism import Mono, Epi
import State
import Atom
from BasicFunctions import Helper
import World
def viererMono(canvas) :

    so = Atom.Atom((2,0),Atom.Verti,Atom.Ker)  # Atom.Atom((1,1),Atom.Verti,Atom.Im)  #Atom.FullOrZeroAtom((1,0),"Full")#  
    go =Atom.FullOrZeroAtom((2,0),Atom.Zero) # Atom.Atom((3,1) , Atom.Hori, Atom.Ker) #Atom.FullOrZeroAtom((2,0),Atom.Zero)
    
    print("wts: vertical map is injective!")
    helper = [Helper.UseUncertaintyForAssumption]
    wld = World.World(canvas, so , go , helper)

    wld.addMorphism(0, 0,0, 1 ,Epi)
    wld.addMorphism(0, 0,1,0)
    wld.addMorphism(1,0, 2, 0)

    #wld.addArea(x, y)
    wld.addMorphism(1, 0,1,1,Mono)
    wld.addMorphism(0,1,1,1)
    wld.addMorphism(1,1,2,1)
    wld.addMorphism(1,0,2,1)


    wld.addMorphism(2, 0, 3, 0)# ,Mono)
    wld.addMorphism(2,0,2,1)

    wld.addMorphism(2, 1, 3, 1)
    wld.addMorphism(3,0,3,1,Mono)
    return wld

def viererEpi(canvas) :

    so =  Atom.FullOrZeroAtom((1,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    go =   Atom.Atom((1,1) , Atom.Verti, Atom.Im) 
    #+ Atom.FullOrZeroAtom((3,1),Atom.Zero) # Atom.Atom((3,1) , Atom.Hori, Atom.Ker) #Atom.FullOrZeroAtom((2,0),Atom.Zero)
    
    
    helper = [Helper.UseUncertaintyForAssumption]
    wld = World.World(canvas, so , go , helper)
    #wld.mm().UP.updateAtom

    wld.addMorphism(0, 0,0, 1 ,Epi)
    wld.addMorphism(0, 0,1,0)
    wld.addMorphism(1,0, 2, 0)

    #wld.addArea(x, y)
    wld.addMorphism(1, 0,1,1)
    wld.addMorphism(0,1,1,1)
    wld.addMorphism(1,1,2,1)


    wld.addMorphism(2, 0, 3, 0)# ,Mono)
    wld.addMorphism(2,0,2,1,Epi)

    wld.addMorphism(2, 1, 3, 1)
    wld.addMorphism(3,0,3,1,Mono)
    return wld

def epiIntro(canvas) :
    so =Atom.FullOrZeroAtom((1,0),"Full")
    go = Atom.Atom((1,0),Atom.Hori,Atom.Im)
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1)
    
    wld.addMorphism(0,0,1,1)
    wld.addAss(Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im))
    wld.addAss(Atom.Atom((1,1),Atom.Verti,Atom.Im) , Atom.Atom((1,1),Atom.Diag,Atom.Im))
    return wld
def kernelInc(canvas) :
    so =  Atom.Atom((0,0),Atom.Diag,Atom.Ker)
    go = Atom.Atom((0,0),Atom.Hori,Atom.Ker)
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1,Mono)
    
    wld.addMorphism(0,0,1,1)
    return wld
    #wld.implications.append((Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im)))
    #wld.implications.append((Atom.Atom((0,0),Atom.Diag,Atom.Ker) , Atom.Atom((0,0),Atom.Hori,Atom.Ker)))
def monoIntro(canvas) :
    so =  Atom.Atom((1,0),Atom.Verti,Atom.Ker)
    go =Atom.FullOrZeroAtom((1,0),"Zero")
    wld = World.World(canvas, so , go )
    wld.addMorphism(0,0,1,0)
    wld.addMorphism(1,0,1,1)
    
    wld.addMorphism(0,0,1,1)
    wld.addAss(Atom.Atom((1,0),Atom.Verti,Atom.Ker) , Atom.Atom((1,0),Atom.Hori,Atom.Im))
    wld.addAss(Atom.Atom((0,0),Atom.Diag,Atom.Ker) , Atom.Atom((0,0),Atom.Hori,Atom.Ker))
    return wld
def add3x3ToWld(wld,avoidRow=0) :
    for x in range(0,3):
        for y in range(0,3) :
            for xi in range(0,2) :
                for yi in range(0,2) :
                    if (x + xi < 3 and y + yi < 3 and (xi > 0 or yi > 0)) :
                        m = None
                        if ((x == 0 and xi == 1) or (y == 0 and yi == 1)) :
                            m = Mono
                        elif ((x+xi == 2 and xi == 1) or (y +yi == 2 and yi == 1) ) :
                            m = Epi
                        if (xi == 1 and yi == 1) : 
                            m = None
                        if (y == avoidRow and y+yi == avoidRow) : 
                            m = None
                        wld.addMorphism(x,y,x+xi,y+yi,m)
    
def nineSurj(canvas) :
    so = Atom.FullOrZeroAtom((2,0),"Full") 
    go = Atom.Atom((2,0),Atom.Hori,Atom.Im)
    """so = Atom.Atom((2,0),Atom.Verti,Atom.Ker)
    go = Atom.FullOrZeroAtom((2,0),"Zero") """
    wld = World.World(canvas,so,go)
    add3x3ToWld(wld)
    return wld
def snakeConstruction(canvas) :
    so =  Atom.Atom((2,0),Atom.Verti,Atom.Ker) #  #Atom.FullOrZeroAtom((2,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    go =   Atom.FullOrZeroAtom((0,2),"Full") #Atom.Atom((0,2) , Atom.Verti, Atom.Im) 
    #+ Atom.FullOrZeroAtom((3,1),Atom.Zero) # Atom.Atom((3,1) , Atom.Hori, Atom.Ker) #Atom.FullOrZeroAtom((2,0),Atom.Zero)
    
    
    helper = [Helper.UseUncertaintyForAssumption]
    wld = World.World(canvas, so , go , helper)
    #wld.mm().UP.updateAtom
    #wld.addSES()
    wld.addMorphism(0, 0,1,0, extra=[Atom.Coker])
    
    

    #wld.addArea(x, y)
    wld.addMorphism(1, 0,1,1)
    #wld.addMorphism(0,1,1,1,Mono)
    wld.addMorphism(1,1,2,1,extra=[Atom.Ker])
    wld.addMorphism(0, 0,0, 1, extra=[Atom.Coker])

    
    wld.addMorphism(2,0,2,1)

    
    
    
    return wld
def cokernelFactorization(canvas) :
    so =  Atom.FullOrZeroAtom((2,0),"Full") #Atom.Atom((2,0),Atom.Verti,Atom.Ker) #  #Atom.FullOrZeroAtom((2,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    go =   Atom.FullOrZeroAtom((2,1),"Full") #Atom.Atom((0,2) , Atom.Verti, Atom.Im) 
    #+ Atom.FullOrZeroAtom((3,1),Atom.Zero) # Atom.Atom((3,1) , Atom.Hori, Atom.Ker) #Atom.FullOrZeroAtom((2,0),Atom.Zero)
    
    
    helper = [Helper.UseUncertaintyForAssumption]
    wld = World.World(canvas, so , go , helper)
    #wld.mm().UP.updateAtom

    wld.addMorphism(0, 0,0, 1)
    wld.addMorphism(0, 0,1,0,extra = [Atom.Coker])
    
    

    #wld.addArea(x, y)
    wld.addMorphism(1, 0,1,1)
    wld.addMorphism(0,1,1,1,extra = [Atom.Coker])
    
    return wld
def obj(canvas) : 
    so =  Atom.FullOrZeroAtom((0,0),"Full") #Atom.Atom((0,0),Atom.Verti,Atom.Ker) #Atom.FullOrZeroAtom((0,1),"Full") #  #Atom.FullOrZeroAtom((2,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    go =  Atom.FullOrZeroAtom((1,0),"Zero") # #Atom.Atom((2,0) , Atom.Verti, Atom.Im)  
    wld = World.World(canvas, so , go)
    wld.addArea(0,0)
    wld.addArea(1,0)
    return wld
def arrow(canvas) :
    so =  Atom.FullOrZeroAtom((0,0),"Full") #Atom.Atom((0,-1),Atom.Verti,Atom.Ker) #Atom.FullOrZeroAtom((0,1),"Full") #  #Atom.FullOrZeroAtom((2,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    go =  Atom.Atom((0,1) , Atom.Verti, Atom.Im)  #  Atom.FullOrZeroAtom((0,1),"Full") #

    helper = [Helper.UseUncertaintyForAssumption]
    wld = World.World(canvas, so , go , helper)
    wld.addMorphism(0, 0,0, 1 ) #,extra = [Atom.Ker] 
     
    
    return wld

def ses(canvas) :
    so =  Atom.FullOrZeroAtom((-1,0),"Full") # Atom.Atom((1,0) , Atom.Hori, Atom.Im)  #
    go =  Atom.FullOrZeroAtom((0,0),"Full") #Atom.Atom((0,0),Atom.Verti,Atom.Ker) #Atom.FullOrZeroAtom((0,1),"Full") #  #Atom.FullOrZeroAtom((2,1),"Full")  #Atom.Atom((1,1),Atom.Hori,Atom.Ker) #   
    wld = World.World(canvas, so , go)
    #wld.addArea(0,0)
    #wld.addSubArea((0,0),(-1,0),Hori,1/3)
   # wld.addMorphism(-1,0,0,0,prop=Mono)
    wld.addSES((0,0),Hori,1/3)
    return wld