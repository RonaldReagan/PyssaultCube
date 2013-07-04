#!/usr/bin/env python

import socket

from consts import *

DEBUG = False

def html_escape(text): #http://wiki.python.org/moin/EscapingHtml
	"""Produce entities within text."""
	return "".join(html_escape_table.get(c,c) for c in text)

def hexdec(s):
	"""return the integer value of a hexadecimal string s"""
	return int(s, 16)
	
def tostr(hs):
	rsp = ''
	for i in range(0, len(hs), 2):
		rsp += chr(hexdec(hs[i] + hs[i+1]))
	return rsp

def getint(p):
	c = ord(p)
	if c == -128: return c
	elif c == -127:
		n = c
		n |= c<<8
		n |= c<<16
		n |= c<<24
		return n
	return c


def decolorize(s):
	while "\f" in s:
		a = s.find("\f")
		b = a+2
		s = s.replace(s[a:b], "") 
	return s

def htmlorize(s):
	code = -1
	s = html_escape(s)
	while "\f" in s:
		code = s[s.find("\f")+1:s.find("\f")+2]
		replacement = ColorCodes[code]
		a = s.find("\f")
		b = s.find("\f")+2
		s = "{0}<span style=\"color:#{1};\">{2}</span>".format(s[:a], replacement, s[b:])
	return s

class ACServer():
	def __init__(self, host, port = 28763):
		self.reset()
		self.host = host
		self.port = port
# 		self.update()
		
	def reset(self):
		self.mode = -1
		self.modename = ''
		self.ord = 0
		self.numplayers = 0
		self.minremain = 0
		self.map = ''
		self.name = ''
		self.maxplayers = 0
		self.pongflags = 0 #probably only used within this part
		self.pongresponse = ''
		self.players = []
		self.data = ''
		self.rawname = ''
		
	def update(self,qtype=1):
		self.reset()
		
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect((self.host, self.port + 1))
		s.settimeout(3)
		s.send(chr(1)+chr(qtype))
		
		data = ''
		self.data = ''
		try:
			data = s.recv(MAXTRANS)
			self.data += data
		except socket.timeout:
			self.reset()
			return "socket timed out"
		except Exception as e:
			return e
		
		#more complex stuff
		self.mode = getint(self.data[5])
		if self.mode > len(MODES):
			self.modename = "ERROR"
			return
		else:
			self.modename = MODES[self.mode + 1]
			
		self.ord = ord(self.data[6])
		self.numplayers = getint(self.data[6])
		self.minremain = getint(self.data[7])
		self.map = ''
		self.name = ''
		i = 8
		while(not ord(self.data[i]) == 0):
			self.map += self.data[i]
			i += 1
			
		i += 1
		
		while(not ord(self.data[i]) == 0):
			self.rawname += self.data[i]
			i += 1
		self.name = decolorize(self.rawname)
		
		i+=1
		self.maxplayers = getint(self.data[i])
		i+=1
		self.pongflags = getint(self.data[i]) #probably only used within this part
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
		
		tmpplayers = data[i:].split('\x00')
		for player in tmpplayers:
			if player is not '':
				self.players.append(player.strip('\x01'))	
		

class ACMS():
	def __init__(self, host='assault.cubers.net', port=28760, extensive=True, sentstr='Pyssaultcube 666'):
		self.extensive = extensive
		self.host = host
		self.port = port
		self.srvlist = []
		self.data = ''
		self.sendstr = sentstr
		self.update(extensive)
		
	def _updateplr_(self):
		self.totalplrs = 0
		for srv in self.srvlist:
			self.totalplrs += srv.numplayers
			if DEBUG: print self.totalplrs
			
	def update(self, fullupdate):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		s.send('list {0}\n'.format(self.sendstr))
		
		self.srvlist = []
		
		while True:
			data = s.recv(1024) 
			if len(data) == 0: 
				break  #EOF 
			self.data += data
		
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