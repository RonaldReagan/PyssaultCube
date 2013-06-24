import os, re
from PIL import Image

from handlers import *

PACKAGESPATH = "./ac/packages"
OUTPUT = "./"+"packages"

validextensions = ('png','jpg')
#Default is a slight hack, as we always strip the / from the start.
specialpaths = {'/default':(blacknwhite,None),r'misc.*':None,r'models/playermodels.*':(saturate,1.0),r'models/pickups.*':(saturate,0.5),'models/misc.*':(saturate,0.5),r'models\/weapons\/.*\/world':(saturate,0.5)}
		
filelists = {}
foundextensions = [] #I use this when determining what file types I am converting. If there is another image format I want to whitelist, I'll see it here.

for h in specialpaths.values():
	if h not in filelists and h != None:
		filelists[h] = []

print("Scanning packages folder...")
for f in os.walk(PACKAGESPATH):
	path,dirs,dirfiles = f
	tfs = [] #temp files
	for f in dirfiles:
		ext = f.split('.')[-1]
		if ext in validextensions:
			tfs.append(os.path.join(path,f))
		if ext not in foundextensions:
			foundextensions.append(ext)
	
	path = path[len(PACKAGESPATH):].strip('/') #Clean it up so we don't have excess '/'s nor PACKAGESPATH
	
	handler = specialpaths['/default']
	for sp in specialpaths: #Detect the handler for this path.
		if re.match(sp,path) != None:
			handler = specialpaths[sp]
			
	if handler == None:
		continue
	
	filelists[handler] += tfs
	
print("Image counts:")
for h in filelists:
	print("  (%s,%s): %d"%(h[0].__name__, repr(h[1]), len(filelists[h])))
	
print("Converting images...")
for h in filelists:
	handle, arg = h
	print("  Converting using handler: (%s,%s)" %(handle.__name__,repr(arg)))
	files = filelists[h]
	for f in files:
		try:
			im = Image.open(f)
		except IOError:
			print("Error opening %s"%f)
			print("    skipping...")
			continue
		
		bpath = f[len(PACKAGESPATH):].strip('/') #Base path, without beginning crud
		path = os.path.join(*bpath.split('/')[:-1])
		try:
			os.makedirs(os.path.join(OUTPUT,path))
		except os.error:
			pass
	
		newim = handle(im,arg)
		newim.save(os.path.join(OUTPUT,bpath))