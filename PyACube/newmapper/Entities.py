import struct

from structformats import ENTITY, Headers
from structio import *


def parseEntities(file,hdr):
	file.seek(sizeOfStruct(Headers[hdr['version']]))
	for i in xrange(hdr['numents']):
		yield readStruct(file, ENTITY)

def packEntities(ents,hdr):
	retstr = ""
	ne = hdr['numents']
	for e in ents:
		if ne == 0:
			break
		ne -= 1
		
		retstr += packStruct( ENTITY, e )
	
	return retstr