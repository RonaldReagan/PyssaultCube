#!/usr/bin/env python
# Program by B}Ronald_Reagan.
# Found at https://github.com/RonaldReagan/PyssaltCube
# License: http://creativecommons.org/licenses/by-nc-sa/3.0/
linecatches = ['blocki', 'block', 'accept', 'bi', 'b', 'a']
blocks = ['blocki', 'block', 'b']
accepts = ['accept', 'a']

def concatlist(set, seperator = ''):
	"""
	Concats a list. List -> String. Kinda hackish, but for its purposes, who gives?
	
	Example:
	>>> concatlist(['I', 'am', 'new', 'here'])
	'Iamnewhere'
	>>>
	>>> concatlist(['I', 'am', 'new', 'here'], ' ')
	'I am new here'
	>>>
	>>> concatlist(['I', 'am', 'new', 'here'], '!')
	'I!am!new!here'
	
	
	"""
	retval = ''
	firstrun = True
	for i in set:
		if firstrun:
			retval = i
			firstrun = False
		else:
			retval = "{0}{1}{2}".format(retval, seperator, i)
	return retval

def CleanNNBL(nnbl, cleanbl, blocklist, acceptlist, appendtent = '', condense = False):
	"""
	Strips a nicknameblacklist of all entries you dont like.
	
	+nnbl is the input file object, or any object with an iter going over each NNBL line.
	+cleanbl is the output file object, or any object with a write method.
	+blocklist is a list with all "block" or "blocki"'s that you want removed from your BL
	+acceptlist is a list with all the "accepts"'s that you want removed from your BL
	+appendtent is a string that will get appended to your BL, this is best for your custom entries
	+condense is a bool controlling the kind of output you want. False just removes the offending
	lines, whereas True tries to strip as much extra fluff from the file. The way it does this is
	kinda hackish, so beware when using this.
	
	Example:
	
	CleanNNBL( open('nnbl.cfg', 'r'), open('nicknamebl.cfg', 'w'), ['B}Clan', 'B}Dinner'], ['B}Ronald_Reagan'])
	
	That will leave the output file almost exactly the same, with all the lines like:
	blocki B}Clan
	block B}Dinner
	accept B}Ronald_Reagan
	a B}Ronald_Reagan
	b B}Clan
	
	and the other variations.
	
	"""
	
	for i in nnbl:
		line = i.strip().split(None, 2)
		if len(line) < 2:
			if not condense: cleanbl.write(i)
			continue
		if condense and line[0][:2] == "//":
			continue
		if line[0] in linecatches:
			if line[0] in blocks and line[1] in blocklist:
				continue
			elif line[0] in accepts and line[1] in acceptlist:
				continue
			else:
				if condense:
					cleanbl.write(concatlist(line[:2], ' ') + chr(10))
					continue
				cleanbl.write(i)
				
		else:
			cleanbl.write(i)
			continue
	cleanbl.write(appendtent)	

def CleanBL(bl, cleanbl, blocklist, appendtent = '', condense = False):
	"""
	See CleanNNBL for description.
	Blocklist is going to be the _exact_ match for the ip.
	Example:
	
	CleanBL(theirbl, mycleanbl, ['0.0.0.0', '0.0.0.0 - 255.255.255.255', '1.2.3.4-5.6.7.8'], condense = True)
	
	Input:
	0.0.0.0 // Stupid ban!!!!
	0.0.0.0 - 255.255.255.255 //WORSE BAN!
	1.2.3.4 - 5.6.7.8 //WEIRDBAN!
	
	Output:
	1.2.3.4 - 5.6.7.8
	"""
	
	for i in bl:
		line = i.strip().split()
		
		if len(line) < 1:
			if not condense: cleanbl.write(i)
			continue
		
		if len(line) >= 3 and line[1] == "-" and line[2][0].isdigit(): #stupid "0.0.0.0 - 255.255.255.255" making things harder
			if concatlist(line[:3], ' ') in blocklist:
				continue
			if condense:
				cleanbl.write(concatlist(line[:3], ' ') + chr(10))
				continue
			
		elif line[0][0].isdigit(): #if the first char _could_ be an IP or not
			if line[0] in blocklist:
				continue
			if condense:
				cleanbl.write(line[0] + chr(10))
				continue
		else:
			if condense: continue
		cleanbl.write(i)
	cleanbl.write(appendtent)

#CleanBL(bl, cleanbl, blblocklist, acceptlist, True)
#CleanNNBL(nnbl, cleanbl, blocklist, acceptlist, True)
if __name__=="__main__":
	import sys
	Condense = False
	
	AppendFile = ''
	if len(sys.argv) < 5:
		print("""
		You need at least four arguments
		BlacklistCleaner.py <operation> <inputpath> <outputpath> <blocklistfile>
		To display the help, do
		BlacklistCleaner.py help
		"""
		sys.exit(1)
	elif len(sys.argv) > 5:
		for i in sys.argv[5:]:
			if i == "-c":
				Condense = True
			elif i[:2] == "-a":
				AppendFile = i[2:]
			else:
				print("Unknown Arugment {0}".format(i))
	blocklistfile = open(sys.argv[4], 'r')
	BLBlockList = []
	for i in blocklistfile:
		BLBlockList.append(i.strip())
	
	#Order of sys args is the same as CleanBL args
	if sys.argv[1]=="bl": #for the BL
		CleanBL(open(sys.argv[2], 'r'), open(sys.argv[3], 'w'), BLBlockList, AppendFile, Condense)
	elif sys.argv[1]=="nnbl":
		CleanNNBL(open(sys.argv[2], 'r'), open(sys.argv[3], 'w'), BLBlockList, AppendFile, Condense)
	elif sys.argv[1]=="help":
		print("""
		You can currently do three different main things, clean a blacklist, clean a nickname blacklist, or show this dialog.
		to clean a blacklist, the format is this:
		BlacklistCleaner.py <operation> <inputpath> <outputpath> <blocklistfile> <extraoptions>
		-operation can be "bl", "nnbl" or "help"
		\tbl will clean an IP blacklist formatted file
		\tnnbl will clean a nickname blacklist formatted file
		\thelp will display this dialog
		-inputpath is the path to the file that will be cleaned
		-outputpath is a path to where you want the final product to be
		-blocklistfile is the file that will provide all of the blocks to be used.
		-extraoptions is extra options you can use:
		\t-c will condense the file to make it slightly smaller in size
		\t-aFILE will append FILE (a path to a file) on to the output file. This would be used for custom blacklist entries.
		"""