#Reads AC map files
import struct
import gzip
from consts import *

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
	x = length-len(stri)
	if x >= 0:
		for i in range(x):
			stri += filler
	else:
		stri = stri[:length]
	return stri

def unpacksqr(kind, file):
	"""
		With a specified kind of square, it unpacks using the file-like object
		pointed to. (will increment the curser)
		Returns an instance of the square.
	"""
	if kind == 0: #Solid
		wtex = (struct.unpack('B', file.read(1))[0])
		vdelta = (struct.unpack('B', file.read(1))[0])
		return Square( kind, wtex = wtex, vdelta = vdelta )
	else:
		floor = struct.unpack('b', file.read(1))[0]
		ceil = struct.unpack('b', file.read(1))[0]
		val = []
		for i in range(0,6):
			val.append(struct.unpack('B', file.read(1))[0])
		return Square( kind, floor = floor, ceil = ceil, wtex = val[0], ftex = val[1], ctex = val[2], vdelta = val[3], utex = val[4], tag = val[5])

class MapError(Exception):
	"""
		Simple error used by the map parser.
	"""
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return repr(self.message)

class Square():
	"""
		Class for the basic square. Also referred to as a cube.
		
		The names closely follow the names used on the AC source.
		
		Main variables:
		kind   = cube type, revalant constants are defined in consts.py
		wtex   = wall texture
		vdelta = delta used for heightfielding, the surface that is heightfielded is specified by the kind
		floor  = floor height
		ceil   = ceiling height
		ftex   = floor texture
		ctex   = ceiling texture
		utex   = upper wall texture
		tac    = gets saved to the map, however is mostly unused and left at 0
	"""
	def __init__(self, kind, wtex = 2, vdelta = 0, floor = 0, ceil = 16, ftex = 3, ctex = 5, utex = 2, tag = 0):
		"""
			Check the full class documentation for a description on the values.
			vdelta, wtex, and kind cannot be None
		"""
		for i in [vdelta, wtex, kind]:
				if i is None:
					raise MapError, "Critical Value is none."
					return
					
		self.kind = kind
		self.wtex = wtex
		self.vdelta = vdelta

		self.floor = floor
		self.ceil = ceil
		self.ftex = ftex
		self.ctex = ctex
		self.utex= utex
		self.tag = tag

	def pack(self):
		"""
			returns the square packed in a save file format
		"""
		#sqr = Square( val[0], floor = val[1], ceil = val[2], wtex = val[3], ftex = val[4], ctex = val[5], vdelta = val[6], utex = val[7], tag = val[8])
		if self.kind == 0:
			return struct.pack('<BBB', self.kind, self.wtex, self.vdelta)
		else:
			return struct.pack('<BbbBBBBBB', self.kind, self.floor, self.ceil, self.wtex, self.ftex, self.ctex, self.vdelta, self.utex, self.tag)
			
	def height(self):
		"""
			Returns the height in cubes
		"""
		return self.ceil - self.floor
			
	def compare(self, sqr):
		"""
			Compares a square to the previous square. Used mainly by the map saving to provide compression.
		"""
		if sqr == None:
			return False
		if self.kind != sqr.kind:
			return False
		if self.kind == sqr.kind and self.wtex == sqr.wtex and self.vdelta == sqr.vdelta:
			if self.kind == 0:
				return True
			elif self.floor == sqr.floor and self.ceil == sqr.ceil and self.ftex == sqr.ftex and self.ctex == sqr.ctex and self.utex == sqr.utex and self.tag == sqr.tag:
				return True
			else:
				return False
		return False
		
	def clone(self):
		"""
			Returns a clone of the square
		"""
		if self.kind == 0:
			return Square( self.kind, wtex = self.wtex, vdelta = self.vdelta)
		else:
			return Square( self.kind, wtex = self.wtex, vdelta = self.vdelta, floor = self.floor, ceil = self.ceil, ftex = self.ftex, ctex = self.ctex, utex = self.utex, tag = self.tag)
	def __repr__(self):
		return "<Cube type {0}>".format(self.kind)
		

class Header():
	"""
		Hold all the header data for the map. Although it could be included in the map class,
		this is kept seperate to be consistant with the AC source.
		
		Main Vars:
		head        - Used by AC. Usually just ACMP
		version     - Map file version. Current supported map revision is kept in consts.py
		headersize  - The headersize, used to read map files. Leave at the default value
		sfactor     - "size factor" the size of the map. The value you use to indicate the size in /newmap <val>
		numents     - the number of entities in the map. IMPORTANT: the map file will be messed up if
		                  this number isn't updated with the entity list before saving.
		maptitle    - the mapmessage
		texlist     - most recently used by textures. Default tex list allows editing. Leave it default unless you
		                  want editor errors
		waterlevel  - the level of the water in the map
		watercolor  - four list of the water color values
		maprevision - the map revision
		ambient     - the ambient light value for the map
		reserved    - not sure what this does, but it is in the mapfile
		mediareq    - "media required"? Used for mappacks, not sure what this exactly does
	"""
	def __init__(self):
		"""
			As of yet, you need to instantiate the class, and then specify the values. Lazy coding
		"""
		#Order is:
		#	head version hdrsize sfactor numents maptitle 
		self.head = "" #0
		self.version = 0 #4
		self.headersize = 1108 #8
		self.sfactor = 0 #12
		self.numents = 0 #16
		self.maptitle = "" #20 len: 128
		self.texlist = [] #1: 148, 2: 404, 3: 660
		for i in range(3):
			self.texlist.append( [] )
			for j in range(256):
				self.texlist[i] = [d for d in range(256)]
		#self.texlist = ["", "", ""] 
		self.waterlevel = 1 #916 len 4
		self.watercolor = [0,0,0,0] #920
		self.maprevision = 0 #924
		self.ambient = 0 #928
		self.reserved = [0,0,0,0,0,0,0,0,0,0,0,0]
		self.mediareq = ""
	def pack(self):
		"""
			Packs the header to save into the map file
		"""
		retstr = '' + packstr(self.head, 4)
		retstr += struct.pack("<iiii", self.version, self.headersize, self.sfactor, self.numents)
		retstr += packstr(self.maptitle, 128)
		for i in self.texlist:
			for j in i:
				retstr += struct.pack("<B", j)
		
		retstr += struct.pack("<i", self.waterlevel)
		for i in self.watercolor:
			retstr += struct.pack("<B", i)
		retstr += struct.pack("<ii", self.maprevision, self.ambient)
		for i in self.reserved:
			retstr += struct.pack("<i", i)
		retstr += packstr(self.mediareq, 128)
		return retstr
	def __repr__(self):
		return "<Header mapversion {0}>".format(self.mapversion)
		
#SIZEOF: 12
#Entity 1: x-16 y-47 z-6 attr1-4 type-1 attr2-11 attr3-16 attr4-21
#X---- Y----- Z----- Attr1-Type a2 a3 a4
#10 00 2F 00 | 06 00 04 00 | 01 0B 10 15
class Entity():
	"""
		Entity class.
		As every kind of entity is stored here, this acts as a reletivly low level container.
		The constants in consts.py will help with the kind, and the attributes for each kind of entity
	"""
	def __init__(self, xyz, attrs, kind):
		self.kind = kind
		self.xyz = xyz
		self.attrs = attrs
		
	def pack(self):
		"""
			Packs the entity to save in the mapfile
		"""
		retstr = ''
		for i in range(3):
			retstr += struct.pack("<h", self.xyz[i])
		retstr += struct.pack("<hBBBB", self.attrs[0], self.kind, self.attrs[1], self.attrs[2], self.attrs[3])
		return retstr
	def __repr__(self):
		return "<Entity kind {0}>".format(self.kind)
		
class ACMap():
	"""
		Main map class. Contains the parser, and various miscellaneous functions.
	"""
	def __init__(self, mappath = '', parse = True, sfactor = 6, mapversion = CURRENTMAPVERSION):
		self.cubelist = []
		self.mappath = mappath
		self.header = Header()
		self.entities = []
		self.defaults = defaults={"wtex":2, "vdelta":0, "floor":0, "ceil":16, "ftex":3, "ctex":5, "utex":2, "tag":0}
		self.defaultsqr = (Square(CubeTypes.SPACE, utex = self.defaults["utex"], tag = self.defaults["tag"], floor = self.defaults["floor"], ftex = self.defaults["ftex"], vdelta = self.defaults["vdelta"], ctex = self.defaults["ctex"], wtex = self.defaults["wtex"], ceil = self.defaults["ceil"] ),Square(CubeTypes.SOLID, wtex = self.defaults["wtex"], vdelta = self.defaults["vdelta"]))
		if parse:
			if self.mappath == '':
				raise MapError, "Have to provide a mappath when parsing!"
			else:
				self.parseCGZ(mappath)
				self.cubeArray = self.return2dlist()
				
		else:
			self.header.sfactor = sfactor
			self.header.version = mapversion
			self.header.head = "ACMP"
			self.header.headersize = 1108
			self.header.numents = 0
			self.maptitle = mappath
			self.populate()
			#print len(self.cubeArray)
			#print len(self.cubeArray[0])
		
	def parseCGZ(self, path):
		"""
			Parses the map file given by path.
		"""
		self.mapname = path.split("/")[-1]
		file = gzip.open(path, "rb")
		
		#We read header here
		self.header.head = file.read(4)
		self.header.version = struct.unpack("i", file.read(4))[0]
		self.header.headersize = struct.unpack("i", file.read(4))[0]
		self.header.sfactor = struct.unpack("i", file.read(4))[0]
		self.header.numents = struct.unpack("i", file.read(4))[0]
		self.header.maptitle = file.read(128).strip('\x00')
		
		for i in range(3):
			for j in range(256):
				self.header.texlist[i][j] = struct.unpack('B', file.read(1))[0]
				
		self.header.waterlevel = struct.unpack("i", file.read(4))[0]
		for i in range (4):
			self.header.watercolor[i] = struct.unpack('B', file.read(1))[0]
		self.header.maprevision = struct.unpack("i", file.read(4))[0]
		self.header.ambient = struct.unpack("i", file.read(4))[0]
		
		if self.header.version <= 2 or self.header.version > CURRENTMAPVERSION :
			raise MapError, "Cannot read/write this mapversion {0}".format(self.header.version)
		
		#This should finish up the header.
		
		#Make sure we are at the right spot.
		file.seek(1108) #TODO: Figure out if this number is going to always be 1108, or the headersize
		
		#SIZEOF: 12
		#Entity 1: x-16 y-47 z-6 attr1-4 type-1 attr2-11 attr3-16 attr4-21
		#X---- Y----- Z----- Attr1-Type a2 a3 a4
		#10 00 2F 00 | 06 00 04 00 | 01 0B 10 15
		
		#Now to the entities
		for i in range(self.header.numents):
			xyz = []
			attrs = []
			for i in range(3):
				xyz.append(struct.unpack("h", file.read(2))[0])
			attrs.append(struct.unpack("h", file.read(2))[0])
			kind = struct.unpack('B', file.read(1))[0]
			for i in range(3):
				attrs.append(struct.unpack('B', file.read(1))[0])
			self.entities.append( Entity(xyz, attrs, kind) )
		
		
		#and now the squares
		while True:
			val = [file.read(1)]
			if val[0] == '':
				break
			val[0] = struct.unpack('B', val[0])[0]
			
			if val[0] == 255: #Compressions
				for i in range(ord(file.read(1))):
					self.cubelist.append( self.cubelist[-1].clone() )
			else:
				self.cubelist.append( unpacksqr(val[0], file) )
		if len(self.cubelist) != self.cubicsize():
			print("Cubicsize is not the same as the cubelist!")
		file.close()
		
		return self
	
	def entitypack(self):
		"""
			Packs all entities for saving.
		"""
		retstr = ''
		for i in self.entities:
			retstr += i.pack()
		return retstr
		
	def packcubes(self):
		"""
			Packs all cubes for saving.
		"""
		retstr = ''
		lastsqr = None
		sc = 0
		snum = 0
		for sqr in self.cubelist:
			snum += 1
			if sqr.compare(lastsqr):
				sc += 1
			else:
				for i in range(sc):
					while sc > 255:
						retstr += struct.pack('<BB', 255, 255)
						sc -= 255
					if sc > 0:
						retstr += struct.pack('<BB', 255, sc)
						sc = 0
				retstr += sqr.pack()
				lastsqr = sqr
		for i in range(sc):
					while sc > 255:
						retstr += struct.pack('<BB', 255, 255)
						sc -= 255
					if sc > 0:
						retstr += struct.pack('<BB', 255, sc)
						sc = 0
		return retstr
			
				
	def writeCGZ(self, path):
		"""
			Writes map to a mapfile specified by the path.
		"""
		if self.header.version <= 2 or self.header.version > CURRENTMAPVERSION :
			raise MapError, "Cannot read/write this mapversion {0}".format(self.header.version)
		file = gzip.open(path, "wb")
		file.write(self.header.pack())
		file.write(self.entitypack())
		file.write(self.packcubes())
		file.close()
	
	def save(self):
		"""
			Overwrites the map that was loaded orginally with current data.
		"""
		self.writeCGZ(self.mappath)
		
	def replacetex(self, kind, oldtex, newtex):
		"""
			Replace all certian textures of a kind with a new texture.
			kind - the kind of texture to replace
				-1 - All
				 0 - wtex
				 1 - ftex
				 2 - ctex
				 3 - utex
			oldtex - the texture number to replace
			newtex - the number to replace it with
		 """
		replacements = 0
		if kind == -1:
			#all
			for sqr in self.cubelist:
				if sqr.wtex == oldtex:
					sqr.wtex = newtex
					replacements += 1
				if sqr.kind == 0:
					continue
				if sqr.ftex == oldtex:
					sqr.ftex = newtex
					replacements += 1
				if sqr.ctex == oldtex:
					sqr.ctex = newtex
					replacements += 1
				if sqr.utex == oldtex:
					sqr.utex = newtex
					replacements += 1
		if kind == 0:
			#wtex
			for sqr in self.cubelist:
				if sqr.wtex == oldtex:
					sqr.wtex = newtex
					replacements += 1
		elif kind == 1:
			#ftex
			for sqr in self.cubelist:
				if sqr.kind == 0:
					continue
				elif sqr.ftex == oldtex:
					sqr.ftex = newtex
					replacements += 1
		elif kind == 2:
			#ctex
			for sqr in self.cubelist:
				if sqr.kind == 0:
					continue
				elif sqr.ctex == oldtex:
					sqr.ctex = newtex
					replacements += 1
		elif kind == 3:
			#utex
			for sqr in self.cubelist:
				if sqr.kind == 0:
					continue
				elif sqr.utex == oldtex:
					sqr.utex = newtex
					replacements += 1
		return replacements
		
	def cubicsize(self):
		"""
			Returns the amount of cubes in the map. It is determined mathmatically rather than by the size of the cube array.
		"""
		ssize = 1<<self.header.sfactor
		return ssize*ssize
		
	def returnIndex(self, x, y):
		"""
			Returns the indice for a 1d array of cubes from an x y coord. Reverse of ACMap.returnXY.
		"""
		ssize = 1<<self.header.sfactor
		return (y * ssize) + x
		
	def returnXY(self, index):
		"""
			Returns the xy coords (of a 2d array) from the given indice (from a 1d array). reverse of ACMap.returnIndex
		"""
		ssize = 1<<self.header.sfactor
		y = int(index / ssize) #Cuts off the remainder
		x = index - (y*ssize)
		return [x, y]
	
	def outofBounds(self, x, y):
		"""
			Determines if the coords given are out of bounds.
		"""
		if self.returnIndex(x, y) >= self.cubicsize():
			return True
			
	def badcube(self, x, y, border = 2):
		"""
			Due to the buggyness of the Cube engine, this determines if a cube is "bad".
			A bad cube is a cube that may have trouble rendering ingame.
			Cube draws a border of 2 around the map.
			
			Border is the border to use.
		"""
		limit = self.returnXY(self.cubicsize()-1)[0]
		if x >= limit-border+1 or y >= limit-border+1:
			return True
		if x <= border or y <= border:
			return True
		return False
	
	def addEnt(self, kind, x, y, z, attr1, attr2, attr3, attr4):
		"""
			Preferred way to add an entity.
			Adds an entity to the entity list and increments the header number of ents.
		"""
		self.entities.append( Entity( [x, y, z], [attr1, attr2, attr3, attr4], kind) )
		self.header.numents += 1
		return len(self.entities)
	
	def rmEnt(self, i):
		"""
			Preferred way to delete an entity.
			Deletes an entity from the entity list and decriements the headers number of ents.
		"""
		del self.entities[i]
		self.header.numents -= 1
		return len(self.entities)
	
	def placeMacro(self, macro, xoffset, yoffset):
		"""
			Old method, should not be used.1
			Places a macro. A macro is a list of cube coords.
			
		"""
		for i in macro:
			sqr = self.cubelist[self.returnIndex(i[0]+xoffset, i[1]+yoffset)]
			sqr.floor = 2
			sqr.ftex = 0
			sqr.wtex = 0
	
	def placeShape(self, coords, sqr=None, includes=None, solid=False):
		"""
			Places a shape on the map.
			coords - The shape. A list of coordinates to modify.
			sqr - The square template (a Square() class) to change the coords to.
			includes - A dictionary of attributes to change.
				'kind' - changes the squares kind to the value given.
				'floor' - changes the squares height by the value given. None makes this the same as the sqr's floor value
				'wtex' - changes the squares wtex to the value given.
				'vdelta' - changes the squares vdelta to the value given.
				'ceil'  - changes the squares ceil height by the value given. None makes this the same as the sqr's ceil value
				'ftex'  - changes the squares ftex to the value given.
				'utex'  - changes the squares utex to the value given.
				'tag' - changes the squares tag to the value given.
			
		"""
		if sqr==None:
			if solid:
				sqr=self.defaultsqr[1]
			else:
				sqr=self.defaultsqr[0]
		if includes==None:
			for coord in coords:
				self.cubeArray[coord[0]][coord[1]] = sqr.clone()
		else:
			for coord in coords:
				cube = self.cubeArray[coord[0]][coord[1]]
				if 'kind' in includes: cube.kind = sqr.kind
				if 'floor' in includes:
					if includes['floor'] != None:
						cube.floor = sqr.floor + includes['floor']
					else:
						cube.floor = sqr.floor
				if 'wtex' in includes: cube.wtex = sqr.wtex
				if 'vdelta' in includes: cube.vdelta = sqr.vdelta
				if 'ceil' in includes:
					if includes['ceil'] != None:
						cube.ceil = sqr.ceil + includes['ceil']
					else:
						 cube.ceil = sqr.ceil
				if 'ftex' in includes: cube.ftex = sqr.ftex
				if 'ctex' in includes: cube.ctex = sqr.ctex
				if 'utex' in includes: cube.utex = sqr.utex
				if 'tag' in includes: cube.tag = sqr.tag
			
	def entstats(self):
		"""
			WIP
			Placeholder
			Will return the same information as /entstats in AC. Possibly as a string, print, or tuple
		"""
		return
		
	def populate(self):
		"""
			Populates the cubelist with the default squares.
			Creates an empty map.
		"""
		if len(self.cubelist) == 0:
			for i in range(self.cubicsize()):
				self.cubelist.append(Square(CubeTypes.SPACE, utex = self.defaults["utex"], tag = self.defaults["tag"], floor = self.defaults["floor"], ftex = self.defaults["ftex"], vdelta = self.defaults["vdelta"], ctex = self.defaults["ctex"], wtex = self.defaults["wtex"], ceil = self.defaults["ceil"] ))
		
		self.cubeArray = self.return2dlist()
		return self

	def placeSolid(self, index):
		"""
			Changes the square at the specified index to the default solid values
		"""
		self.cubelist[index] = Square(CubeTypes.SOLID, wtex = self.defaults["wtex"], vdelta = self.defaults["vdelta"])
	def placeSpace(self, index):
		self.cubelist[index] = Square(CubeTypes.SPACE, utex = self.defaults["utex"], tag = self.defaults["tag"], floor = self.defaults["floor"], ftex = self.defaults["ftex"], vdelta = self.defaults["vdelta"], ctex = self.defaults["ctex"], wtex = self.defaults["wtex"], ceil = self.defaults["ceil"] )
	
	def returnSpace(self):
		"""
			Changes the square at the specified index to the default space (empty values
		"""
		return Square(CubeTypes.SPACE, utex = self.defaults["utex"], tag = self.defaults["tag"], floor = self.defaults["floor"], ftex = self.defaults["ftex"], vdelta = self.defaults["vdelta"], ctex = self.defaults["ctex"], wtex = self.defaults["wtex"], ceil = self.defaults["ceil"] )
	
	def returnSolid(self):
		"""
			Returns the default solid square.
		"""
		return Square(CubeTypes.SOLID, wtex = self.defaults["wtex"], vdelta = self.defaults["vdelta"])
	
	def return2dlist(self):
		"""
			Returns a 2d list (array) of the cubes.
		"""
		retlist = []
		#cubelist = list(self.cubelist) #make a copy so we dont mess anything up
		sqrcounter = 0
		
		for y in range(1<<self.header.sfactor):
			retlist.append( [] )
			
			for x in range(1<<self.header.sfactor):
				retlist[y].append(self.cubelist[sqrcounter])
				sqrcounter += 1
		return retlist
			
	
	def __repr__(self):
		return "<{0} sfactor {1}>".format(self.mappath, self.header.sfactor)
	
	def __iter__(self):
		return iter(self.cubelist)
		
	def __len__(self):
		return len(self.cubelist)
	def __getitem__(self, i):
		return self.cubelist[i]
	def __getslice__(self, i, j):
		return self.cubelist[i,j]
				
# This is pending review of my method and its accuracy.
#def rectangle(xya, xyb):
#	retlist = []
#	xa,ya = xya
#	xb,yb = xyb
#	l = xb - xa
#	w = yb - ya
#	
#	if l == 0:
#		for i in range(w+1):
#			retlist.append((xa, ya+i))
#	elif w == 0:
#		for i in range(l+1):
#			retlist.append((xa+i, ya))
#	else:
#		for j in range(w + 1):
#			for i in range(l + 1):
#				retlist.append((xa+j, ya + i))
#	
#	return retlist
			
def cubicsize(sfactor):
	"""
		Same as ACMap.cubicsize
	"""
	ssize = 1<<sfactor
	return ssize*ssize
