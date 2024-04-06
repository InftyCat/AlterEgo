#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:48:27 2024

@author: tim
"""

        ax = self.areas[(x1,y1)]
        ay =self.areas[(x2,y2)]
        d = Atom.getDir(x1,y1,x2,y2)
        
        segs = ay.findAllSegments(d,True)
        sidx = 0
        tidx = len(segs) - 1
        
        while (not (Bsc.inList(segs[sidx].src() , ax.getPoints() , Bsc.comPnts))) :
            sidx +=1
        while (not (Bsc.inList(segs[tidx].trg() , ax.getPoints() , Bsc.comPnts))) :
            tidx -=1
        segs = segs[sidx:tidx+1] #list(filter(lambda s : Bsc.inList(s.src() , ay.getPoints() , Bsc.comPnts) ,  ))
        xstart = (segs[0].x1,segs[0].y1)
        xend = (segs[-1].x2,segs[-1].y2)
        print("xstart/end",xstart,xend)
        self.canvas.create_circle_arc(*xstart,20,start = 0,end = 359,fill="black")
        self.canvas.create_circle_arc(*xend,30,start = 0,end = 359,fill="white")
        istart = list(filter (lambda  i : Bsc.comPnts(ax.segments[i].trg() , xend) ,  range(len(ax.segments))))
        iend = list(filter (lambda i : Bsc.comPnts(ax.segments[i].src() , xstart) , range(len(ax.segments))))
        if (len(istart) * len(iend) == 0) :
            print("create kernel error" )
        else :
            if (len(istart) != 1):
                print ("weird s",[str(ax.segments[i]) for i in istart])
            if (len(iend) != 1) :
                print ("werid end")
            istart = istart[0]
            iend =iend[0] + 1
            #print(istart,iend)
            segs2 = getSubList(istart,iend,ay.segments)
            
            ker= Area.Area(self.canvas,ax.c,ax.w*1.5)
            for s in segs : #+ segs2 :
                ker.stealSegment(s)
                    
            return ker



 def applyAssMonoEpi(self) :
        r = self.mm().subobject().getRoom()
        morIn = [value for key, value in self.morphs.items() if value.trg() == r and value.prop== Morphism.Epi]
        morOut = [value for key, value in self.morphs.items() if value.src() == r and value.prop == Morphism.Mono]
        mor = morOut + morIn
        #print("morphs:" , len(mor), "room",r)
        if (self.assCnt < len(mor)) :
            m = mor[self.assCnt]
            subobj = m.subobject()
            if self.assCnt < len(morOut) :
                print("checking monomorphism")
                if self.subobject().atom == subobj :
                    print("apply mono goal")
                    self.mm().updateStateFromSubobj(FullOrZeroAtom(r, Zero))
            else :                
                    self.mm().updateStateFromSubobj(mor[self.assCnt].subobject())
            self.assCnt += 1
        else :
            self.assCnt = 0
            """
            if self.areas[r].exactHori :
                if self.subobject().info == Ker :    
                    self.updateAtom(Atom.Atom(r,self.subobject().mdir,Im))
                elif self.subobject().info == Im :
                    self.updateAtom(Atom.Atom(r,self.subobject().mdir,Ker))
                    """
        #print("used assumption atom:" , self.mm().subobject())
            # todo exactness
     