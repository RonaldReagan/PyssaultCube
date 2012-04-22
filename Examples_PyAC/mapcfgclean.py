#Takes a map and config file and removes all unnecessary textures, mapmodels and sounds.
# To use, change the variable mapname to your mapname without the suffix. Make sure the map is in: ./sourcefiles/maps/
# Your cleaned file will appear in the ./results directory as mapname_clean.cfg and mapname_clean.cgz
mapname = "mapname"


try:
	#First try to import from the main installed package
	from PyACube.mapfiles.cgz import *
	from PyACube.mapfiles.cfg import *
	from PyACube.mapfiles.consts import *
except ImportError:
	#Then assume we are in the examples folder.
	import sys; sys.path.insert(0, "..")
	from PyACube.mapfiles.cgz import *
	from PyACube.mapfiles.cfg import *
	from PyACube.mapfiles.consts import *

ac_map = ACMap("sourcefiles/maps/%s.cgz" %mapname)
ac_cfg = MapCFG("sourcefiles/maps/%s.cfg" %mapname)

mapmodellist = []
soundlist = []
texturelist = []

delmapmodellist = []
delsoundlist = []
deltexturelist = []

delmapmodeldict = {}
delsounddict = {}
deltexturedict = {}

#Datacollection phase:
for i in ac_map.entities:
	if i.kind == EntTypes.MAPMODEL:
		if i.attrs[1] not in mapmodellist:
			mapmodellist.append(i.attrs[1])
	elif i.kind == EntTypes.SOUND:
		if i.attrs[0] not in soundlist:
			soundlist.append(i.attrs[0])
for sqr in ac_map:
	texset = [sqr.wtex, sqr.ftex, sqr.ctex, sqr.utex]
	for i in texset:
		if i not in texturelist:
			texturelist.append(i)
			
for i in range(len(ac_cfg.mapmodels)):
	if i not in mapmodellist:
		delmapmodellist.append(i)
for i in range(len(ac_cfg.sounds)):
	if i not in soundlist:
		delsoundlist.append(i)
for i in range(len(ac_cfg.textures)):
	if i not in texturelist:
		deltexturelist.append(i)

#END datacollection phase

#Prep phase
mmdamt = 0 #Mapmodel delete amount
for i in range(len(ac_cfg.mapmodels)):
	if i in delmapmodellist:
		mmdamt += 1
	delmapmodeldict[i] = mmdamt

sdamt = 0
for i in range(len(ac_cfg.sounds)):
	if i in delsoundlist:
		sdamt += 1
	delsounddict[i] = sdamt

tdamt = 0
for i in range(len(ac_cfg.textures)):
	if i in deltexturelist:
		tdamt += 1
	deltexturedict[i] = tdamt

#END prep phase

#Clean phase
		
for i in ac_map.entities:
	if i.kind == EntTypes.MAPMODEL:
		i.attrs[1] -= delmapmodeldict[i.attrs[1]]
	elif i.kind == EntTypes.SOUND:
		i.attrs[0] -= delsounddict[i.attrs[0]]
		
for sqr in ac_map:
	sqr.wtex -= deltexturedict[sqr.wtex]
	sqr.ftex -= deltexturedict[sqr.ftex]
	sqr.ctex -= deltexturedict[sqr.ctex]
	sqr.utex -= deltexturedict[sqr.utex]

for texlist in ac_map.header.texlist:
	for i in range(len(texlist)):
		texlist[i] -= deltexturedict[texlist[i]]

 
deletes = 0
for i in delmapmodellist:
	del ac_cfg.mapmodels[i-deletes]
	deletes += 1

deletes = 0
for i in delsoundlist:
	del ac_cfg.sounds[i-deletes]
	deletes += 1

deletes = 0
for i in deltexturelist:
	del ac_cfg.textures[i-deletes]
	deletes += 1

ac_map.writeCGZ("results/%_clean.cgz" %mapname)
ac_cfg.writeCFG("results/%_clean.cfg" %mapname)