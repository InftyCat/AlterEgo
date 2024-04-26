import BasicFunctions as Bsc
class Room :
    def __init__ (self,  _room=None ,_infty=False) :
        
        self.room = _room
        self.infty = _infty
    def __str__ (self) :
         if self.infty :
              return "°"
         else :
              return "[" + str(self.room) + "]"
    def setToInfty(self) : 
        self.infty = True
        self.room = None
    def wedge(self,wld,room) :
         if isinstance(room, Room) :
            if room.infty :
                self.setToInfty()
                return
            else :
                 room = room.room
         #print(self.room,room)
         if not self.infty :
                m = wld.safeMax([self.room , room])
                if (m != None) : 
                     self.room = m
                else :                
                     self.setToInfty()
    def isDeeperThan(self,wld,room) :
         if (self.infty) :
              return True
         else :
                if (room.infty) : 
                   return False
                else :
                     return wld.maximum([room.room,self.room]) == self.room
"""def wedge(self, room) :
        if (self.genus == Genus.Unc) :
            self.room.wedge(room)
            if self.info != Full :
                return Bsc.maximum([self.getCoRoom() , room])
            else :
                return None
        else :
            print("wedge error")
            """