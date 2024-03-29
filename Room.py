import BasicFunctions as Bsc
class Room :
    def __init__ (self, _room=None ,_infty=False) :
        
        self.room = _room
        self.infty = _infty
    def __str__ (self) :
         if self.infty :
              return "°"
         else :
              return "[" + str(self.room) + "]"
    def wedge(self,room) :
         if isinstance(room, Room) :
            if room.infty :
                self.infty = True
                self.room = None
                return
            else :
                 room = room.room
         print(self.room,room)
         if not self.infty :
                self.room = Bsc.maximum([self.room , room])
"""def wedge(self, room) :
        if (self.genus == Unc) :
            self.room.wedge(room)
            if self.info != Full :
                return Bsc.maximum([self.getCoRoom() , room])
            else :
                return None
        else :
            print("wedge error")
            """