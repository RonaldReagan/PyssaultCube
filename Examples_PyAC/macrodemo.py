try:
	#First try to import from the main installed package
	from PyACube.mapfiles.cgz import ACMap
	from PyACube.mapfiles.macros import *
except ImportError:
	#Then assume we are in the examples folder.
	import sys; sys.path.insert(0, "..")
	from PyACube.mapfiles.cgz import ACMap
	from PyACube.mapfiles.macros import *

mappath = "./results/macrodemo.cgz"

acmap = ACMap(parse = False, sfactor = 7, maptitle = "\f3PyACube Macro Demo")

style = {'floor': 1, 'ftex': 12, 'wtex': 12}

for i, macro in enumerate(letters_small[:8]):
	acmap.placeShape(macro, ((i*6)+40, 30), includes=style)

for i, macro in enumerate(letters_small[8:17]):
	acmap.placeShape(macro, ((i*6)+40, 40), includes=style)

for i, macro in enumerate(letters_small[17:]):
	acmap.placeShape(macro, ((i*6)+40, 50), includes=style)

for i, macro in enumerate(letters_large[:8]):
	acmap.placeShape(macro, ((i*6)+40, 70), includes=style)

for i, macro in enumerate(letters_large[8:17]):
	acmap.placeShape(macro, ((i*6)+40, 80), includes=style)

for i, macro in enumerate(letters_large[17:]):
	acmap.placeShape(macro, ((i*6)+40, 90), includes=style)
	
acmap.drawBorder()
acmap.header.ambient = 100
acmap.header.waterlevel = -1

acmap.writeCGZ(mappath)
