import struct

TYPE_INT = 0 #implied len of 4
TYPE_INTLIST = 1
TYPE_UINT = 2
TYPE_UINTLIST = 3
TYPE_STR = 4 #Strips 'filler' off of the string. Defaults to '\x00'. Packs with filler.
TYPE_VSTR = 5 #Variable length string, takes the length provided by struct value named in 'size'.
TYPE_UCHAR = 6
TYPE_UCHARLIST = 7 #implied len of 1
TYPE_CHAR = 8
TYPE_CHARLIST = 9
TYPE_SHORT = 10
TYPE_USHORT = 11

def packstr(stri, length, filler = '\x00'):
	"""
		Will pack a string for the map format.
		stri   - the content
		length - the space allotted
		filler - the filler for excess space if needed.
		
		>>> packstr("ACMP", 10, filler = "!")
		'ACMP!!!!!!'
		
		As viewed in a hex viewer:
		41 43 4D 50 21 21 21 21 21 21
		
	"""
	return stri[:length].ljust(length,filler)

def sizeOfStruct(structformat):
	total = 0
	for item in structformat:
		if item['type'] in [TYPE_INT,TYPE_UINT]:
			total += 4
		elif item['type'] in [TYPE_INTLIST,TYPE_UINTLIST]:
			total += 4*item['len']
		elif item['type'] == TYPE_STR:
			total += item['len']
		elif item['type'] == TYPE_VSTR:
			total += item.get('maxlen',0) #If maxlen provided use this. Probably not the method when using structs with VSTR's
		elif item['type'] in [TYPE_UCHAR,TYPE_CHAR]:
			total += 1
		elif item['type'] in [TYPE_UCHARLIST,TYPE_CHARLIST]:
			total += item['len']
		elif item['type'] in [TYPE_SHORT,TYPE_USHORT]:
			total += 2
	
	return total

def readStruct(file, structformat,endian="<",filters=["_unused_"]):
	retdict = {}
	
	for item in structformat:
		skip = False
		for f in filters:
			if item.get(f,False):
				retdict[item['name']] = item.get('default',None)
				skip = True
		
		if skip:
			continue
			
		if item['type'] == TYPE_INT:
			retdict[item['name']] = struct.unpack(endian+"i", file.read(4))[0]
			
		elif item['type'] == TYPE_INTLIST:
			retdict[item['name']] = struct.unpack(endian+"i"*item['len'], file.read(4*item['len']))
		
		if item['type'] == TYPE_UINT:
			retdict[item['name']] = struct.unpack(endian+"I", file.read(4))[0]
			
		elif item['type'] == TYPE_UINTLIST:
			retdict[item['name']] = struct.unpack(endian+"I"*item['len'], file.read(4*item['len']))
			
		elif item['type'] == TYPE_STR:
			s = str(file.read(item['len']))
			filler = item.get('filler','\x00')
			if filler:
				s = s.strip(filler)
				
			retdict[item['name']] = s
		
		elif item['type'] == TYPE_VSTR:
			length = retdict[item['size']]
			s = str(file.read(length))
			filler = item.get('filler','\x00')
			if filler:
				s = s.strip(filler)
				
			retdict[item['name']] = s
			
		elif item['type'] == TYPE_UCHAR:
			retdict[item['name']] = struct.unpack(endian+"B", file.read(1))[0]
			
		elif item['type'] == TYPE_UCHARLIST:
			retdict[item['name']] = struct.unpack(endian+"B"*item['len'], file.read(item['len']))
		
		elif item['type'] == TYPE_CHAR:
			retdict[item['name']] = struct.unpack(endian+"b", file.read(1))[0]
		
		elif item['type'] == TYPE_CHARLIST:
			retdict[item['name']] = struct.unpack(endian+"b"*item['len'], file.read(item['len']))
	
		elif item['type'] == TYPE_SHORT:
			retdict[item['name']] = struct.unpack(endian+"h", file.read(2))[0]
			
		elif item['type'] == TYPE_USHORT:
			retdict[item['name']] = struct.unpack(endian+"H", file.read(2))[0]
	
	return retdict

def packStruct(structformat, struct,endian="<",filters=["_unused_"]):
	retstr = ""
	
	for item in structformat:
		skip = False
		for f in filters:
			if item.get(f,False):
				skip = True
		
		if skip:
			continue
			
		name = item['name']
		
		if name not in struct:
			skip = True
			default = item.get('default',None)
			if default != None:
				struct[name] = default
		
		if 'sizeof' in item:
			struct[name] = len(struct[item['sizeof']])
			
		if item['type'] == TYPE_INT:
			retstr += struct.pack(endian+"i",struct[name])
			
		elif item['type'] == TYPE_INTLIST:
			retstr += struct.pack(endian+"i"*item['len'],*struct[name])
			
		if item['type'] == TYPE_IINT:
			retstr += struct.pack(endian+"I",struct[name])
			
		elif item['type'] == TYPE_IINTLIST:
			retstr += struct.pack(endian+"I"*item['len'],*struct[name])
			
		elif item['type'] == TYPE_STR:
			retstr += packstr(struct[name],item['name'],filler=item.get('filler','\x00'))
			
		elif item['type'] == TYPE_UCHAR:
			retstr += struct.pack(endian+"B",struct[name])
			
		elif item['type'] == TYPE_UCHARLIST:
			retstr += struct.pack(endian+"B"*item['len'],*struct[name])
		
		elif item['type'] == TYPE_CHAR:
			retstr += struct.pack(endian+"b",struct[name])
			
		elif item['type'] == TYPE_CHARLIST:
			retstr += struct.pack(endian+"b"*item['len'],*struct[name])
		
		elif item['type'] == TYPE_SHORT:
			retstr += struct.pack(endian+"h",struct[name])
		
		elif item['type'] == TYPE_USHORT:
			retstr += struct.pack(endian+"H",struct[name])
	
	return retstr