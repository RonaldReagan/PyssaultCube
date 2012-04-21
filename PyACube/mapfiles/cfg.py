#A config parser for AC maps.
import string

def cleanpathline(path):
	"""
		Cleans a line extracting just the path. Returns a string.
	"""
	quotes = False
	path = path.strip() #Replace is in place becase of the commonality of tabs and spaces
	path = path.replace('\t', '')
	path = path.replace(' ', '')
	
	for i in range(len(path)):
		if path[i] == '"' or path[i] == "'":
			if not quotes:
				quotes = True
			else:
				quotes = False
		elif path[i] + path[i+1] == "//" and not quotes:
			path = path[:i].strip()
			break
	return path.replace('"', '').replace("'", '')

def formatpathline(path):
	"""
		Formats a path to include quotes. Returns a string.
	"""
	return '"' + path + '"'

def cleanintline(line, base = 10):
	"""
		Cleans a line containing an integer. Reterns an int
	"""
	retstr = ''
	line = line.strip()
	#print len(line)
	for i in range(len(line)):
		try:
			if line[i] + line[i+1] == "//":
				break
			elif line[i] in string.digits + '-': #digits or a negative sign
				retstr += line[i]
		except IndexError:
			retstr += line[i]
			
	return int(retstr, base)

	
class Mapmodel():
	"""
		Basic class for a mapmodel. The format is usually:
		mapmodel 2 2 0 0 "nothing"
		sqrad - arg1
		bbhght - arg2
		ihght - arg3
		arg4 is always 0
		path - arg5
	"""
	def __init__(self, sqrad, bbhght, ihght, path):
		self.path = path
		self.sqrad = sqrad
		self.bbhght = bbhght
		self.ihght = ihght
	def pack(self): #Possibly a misnomer
		"""
			Formats the string for use in a cfg file. Returns a string
		"""
		return 'mapmodel {0} {1} {2} 0 "{3}"'.format(self.sqrad, self.bbhght, self.ihght, self.path)
	
class Texture(): #texture 0 "kurt/klite1.jpg"
	def __init__(self, scale, path):
		self.path = path
		self.scale = scale
		
	def pack(self): #Possibly a misnomer
		return "texture {scale} {path}".format(scale = self.scale, path = formatpathline(self.path))

class Sound():#mapsound "ambience/cavedrip.ogg" -1
	def __init__(self, path, maxsim):
		self.path = path
		self.maxsim = maxsim
	def pack(self):
		return "mapsound {0} {1}".format( formatpathline(self.path), self.maxsim )

class MapCFG(): #loadnotexture loadsky mapmodelreset mapmodel texturereset texture fog fogcolour mapsoundreset mapsound watercolour shadowyaw
	def __init__(self, cfgpath):
		self.path = cfgpath
		self.mapmodels = []
		self.textures = []
		self.sounds = []
		self.sky = ''
		self.fog = -1 #If it remains -1, it indicates that it never got found in the cfg.
		self.fogcolour = -1
		self.watercolour = [-1, -1, -1]
		self.shadowyaw = -1
		self.WTFs = []
		self.parseCFG(self.path)
		
	def parseCFG(self, path):
		cfg = open(path, 'r')
		for linee in cfg:
			#linee = dirty version of the line
			#line = clean, split version of the line
			
			#if "\n" in line: print "hhhhhh"
			args = []
			linee = linee.strip()
			#if line[:2] == "//": #Comments
			#	continue
			line = linee.split(' ', 1)
			if line[0] == "mapmodel": #R H Z 0 N
				for i in range(5): #Cutesy way to strip the arguments
					line = line[1].strip().split(' ', 1)
					args.append(line[0].strip())
				
				self.mapmodels.append( Mapmodel(int(args[0]), int(args[1]), int(args[2]), cleanpathline(args[4])) ) 
			
			elif line[0] == "loadsky": #P
				self.sky = cleanpathline(line[1])
			
			elif line[0] == "texture":
				for i in range(2):
					line = line[1].strip().split(' ', 1)
					args.append(line[0].strip())
				self.textures.append( Texture(int(args[0]), cleanpathline(args[1])) )
			
			elif line[0] == "mapsound":
				for i in range(2):
					line = line[1].strip().split(' ', 1)
					args.append(line[0].strip())
				self.sounds.append( Sound(cleanpathline(args[0]), int(cleanintline(args[1]))) ) 
			
			elif line[0] == "fog":
				self.fog = int(cleanintline(line[1]))
			
			elif line[0] == "fogcolour":
				self.fogcolour = int(cleanintline(line[1], 16))
				
			elif line[0] == "watercolour":
				for i in range(3):
					line = line[1].strip().split(' ', 1)
					args.append(cleanintline(line[0].strip()))
				self.watercolour = [args[0],args[1],args[2]]
			
			elif line[0] == "shadowyaw":
				shadowyaw = int(cleanintline(line[1]))
			
			elif line[0] not in "loadnotexture mapmodelreset texturereset mapsoundreset": #"We dont know this command!"
				self.WTFs.append(linee)
		cfg.close()
	
	def writeCFG(self, path, wtfs=0):
		cfg = open(path, "w")
		
		if wtfs == 1:
			for i in self.WTFs:
				cfg.write("%s\n" %i)
		if self.fog != -1:
			cfg.write("fog %d\n" %self.fog)
		if self.fogcolour != -1:
			cfg.write("fogcolour %x\n" %self.fogcolour)
		for item in self.watercolour:
			if item != -1:
				cfg.write("watercolour %d %d %d\n" %(self.watercolour[0], self.watercolour[1], self.watercolour[2] ))
				break
		if self.shadowyaw != -1:
			cfg.write("shadowyaw %d\n" % self.shadowyaw)
		
		if self.sky != '':
			cfg.write("loadsky %s\n" % formatpathline(self.sky) )
		cfg.write("\n")
			
		cfg.write("\nloadnotexture\ntexturereset\n")
		#Now for the looping
		for i in range(len(self.textures)):
			cfg.write("{0} //Texture #{1}\n".format(self.textures[i].pack(), i ))
			
		cfg.write("\nmapmodelreset\n")
		for i in range(len(self.mapmodels)):
			cfg.write("{0} //Mapmodel #{1}\n".format(self.mapmodels[i].pack(), i ))
			
		cfg.write("\nmapsoundreset\n")
		for i in range(len(self.sounds)):
			cfg.write("{0} //Mapsound #{1}\n".format(self.sounds[i].pack(), i ))
		
		if wtfs == 2:
			for i in self.WTFs:
				cfg.write("%s\n" %i)
			
		cfg.close()