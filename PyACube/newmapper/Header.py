import struct

from structformats import *
from structio import *

from maperror import *

def parseHeader(file):
	file.seek(0)
	head = file.read(4)
	version = struct.unpack("i", file.read(4))[0]
	
	if version not in Headers:
		raise MapVersionError(version)
		return None
	
	header = readStruct(file,Headers[version])
	header['head'] = head
	header['version'] = version
	
	return header

def packHeader(header):
	retstr = ""
	retstr += packstr(header['head'],4)
	retstr += struct.pack("<i",header['version'])
	
	retstr += packStruct( Headers[header['version']], header )
	
	return retstr