#!/usr/bin/env python

import socket

from .. import cbuffer
from consts import *

def getint(pb):
    c = pb.get()
    if c == -128:
        n = pb.get()
        n |= pb.get()<<8
        return n
    elif c == -127:
        n = pb.get()
        n |= pb.get()<<8
        n |= pb.get()<<16
        n |= pb.get()<<24
        return n
    else:
        return c

class ACServer():
    def __init__(self, host, port = 28763):
        self.reset()
        self.host = host
        self.port = port
        self.update()
        
    def reset(self):
        self.mode = None
        self.ord = 0
        self.numplayers = 0
        self.minremain = 0
        self.map = ''
        self.name = ''
        self.maxplayers = 0
        self.pongflags = 0 #probably only used within this part
        self.pongresponse = 0
        self.players = []
        self.data = ''
        self.rawname = ''
        self.error = None
    
    def getData(self,qtype):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((self.host, self.port + 1))
            s.settimeout(3)
            s.send(chr(1)+chr(qtype))
            data = s.recv(MAXTRANS)
        except (socket.timeout, socket.error, socket.herror, socket.gaierror) as e:
            self.reset()
            self.error = e
            return None
        
        self.error = None
        return data
        
        
    def update(self):
        """
            Updates information.
            If there is a problem (most likely timeout) returns False. Else returns True
        """
        self.reset()
        self.data = self.getData(1)
        
        if self.data == None:
            return False
        
        buf = cbuffer.PacketBuffer(self.data)
        self.ping = buf.getInt()
        self.query = buf.getInt()
        self.protocol = buf.getInt()
        self.mode = buf.getInt()
        self.numplayers = buf.getInt()
        self.minremain = buf.getInt()
        self.map = buf.getStr()
        self.name = buf.getStr()
        
        self.maxplayers = buf.getInt()
        self.pongflags = buf.getInt() #probably only used within this part
        self.pongresponse = ''
        
        if self.pongflags > 0:
            mm = self.pongflags >> 6
            
            if self.pongflags & (1 << 1):
                self.pongresponse = PF_BANNED
            if self.pongflags & (1 << 2):
                self.pongresponse = PF_BLACKLISTED
            elif self.pongflags & (1 << 0):
                self.pongresponse = PF_PASSPROTECTED
            elif mm:
                self.pongresponse = MasterModes[mm]
        
#         #FIXME: Hackish and probably will bug up once and awhile.

        if buf.getInt() == self.query: #Namelist
            for player in xrange(self.numplayers):
                player = buf.getStr()
                self.players.append(player)
        
        return True
        

class ACMS():
    def __init__(self, host='assault.cubers.net', port=28760, extensive=True, sentstr='Pyssaultcube 42'):
        self.extensive = extensive
        self.host = host
        self.port = port

        self.sendstr = sentstr
        self.update(extensive)
    
    def reset(self):
        self.error = None
        self.srvlist = []
        self.data = ''
        self.totalplrs = 0
        self.numsrvs = 0
        
    def _updateplr_(self):
        self.totalplrs = 0
        for srv in self.srvlist:
            self.totalplrs += srv.numplayers
        
    def getData(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.send('list {0}\n'.format(self.sendstr))
        
            data = ""
            while True:
                d = s.recv(1024) 
                if len(d) == 0: 
                    break  #EOF 
                data += d
        except (socket.timeout, socket.error, socket.herror, socket.gaierror) as e:
            self.reset
            self.error = e
            return None
            
        self.error = None
        return data
            
    def update(self, fullupdate):
        self.reset()
        self.data = self.getData()
        
        if self.data == None:
            return False
        
        for i in self.data.split("\n"):
            if i[0] != "a":
                break
                
            tmpsrv = i.split()
            del tmpsrv[0]
            if self.extensive:
                self.srvlist.append( ACServer(tmpsrv[0], int(tmpsrv[1])) )
            else:
                self.srvlist.append( (tmpsrv[0], tmpsrv[1]) )
        self.numsrvs = len(self.srvlist)
        if fullupdate:
            self._updateplr_()
        
        return True