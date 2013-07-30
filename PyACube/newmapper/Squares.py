import struct

from structformats import SQUARE,ENTITY,Headers
from structio import *

from maperror import *
		
def parseSquares(file,hdr):
	file.seek(sizeOfStruct(Headers[hdr['version']])+(sizeOfStruct(ENTITY)*hdr['numents']))
	ns = 0
	while ns != getCubicSize(hdr):
		val = file.read(1)
		if val == '':
			raise MapError("File corrupted, i=%d"%i)
		
		val = struct.unpack('<B', val)[0]
		
		sqr = None
		if val == 255:
			for i in range(ord(file.read(1))):
				ns += 1
				yield sqr
		else:
			if val == 0: #Solid
				sqr = readStruct(file, SQUARE, filters=["_unused_","_spaceonly_"])
			else:
				sqr = readStruct(file, SQUARE)
				
			sqr['kind'] = val
			
			ns += 1
			yield sqr

def getCubicSize(hdr):
	ssize = getSideSize(hdr)
	return ssize*ssize
	
def getSideSize(hdr):
	return 1<<hdr['sfactor']

def getPos(i,hdr):
	ssize = getSideSize(hdr)
	y = int(index / ssize) #Gets floored.
	x = index - (y*ssize)
	return (x, y)

def compareSquare(sqrA, sqrB):
	"""
		Compares a square to the previous square. Used mainly by the map saving to provide compression.
		
		:rtype: Bool
	"""
	if sqrB == None:
		return False
	if sqrA['kind'] != sqrB['kind']:
		return False
	if sqrA['kind'] == sqrB['kind'] and sqrA['wtex'] == sqrB['wtex'] and sqrA['vdelta'] == sqrB['vdelta']:
		if sqrA['kind'] == 0:
			return True
		elif sqrA['floor'] == sqrB['floor'] and sqrA['ceil'] == sqrB['ceil'] and sqrA['ftex'] == sqrB['ftex'] and sqrA['ctex'] == sqrB['ctex'] and sqrA['utex'] == sqrB['utex'] and sqrA['tag'] == sqrB['tag']:
			return True
		else:
			return False
	return False

def packSquares(sqrs):
	retstr = ""
	lastsqr = None
	sc = 0
	for s in sqrs:
		if compareSquare(lastsqr,s):
			sc += 1
		else:
			for i in xrange(sc): #Flush compression square count
				while sc > 255:
					retstr += struct.pack('<BB', 255, 255)
					sc -= 255
				if sc > 0:
					retstr += struct.pack('<BB', 255, sc)
					sc = 0
			
			if s['kind'] == 0: #Solid
				retstr += packStruct( SQUARE, s, filters=["_spaceonly_"] )
			else:
				retstr += packStruct( SQUARE, s )
			
			lastsqr = s
	
	for i in range(sc):
		while sc > 255:
			retstr += struct.pack('<BB', 255, 255)
			sc -= 255
		if sc > 0:
			retstr += struct.pack('<BB', 255, sc)
			sc = 0
	
	return retstr