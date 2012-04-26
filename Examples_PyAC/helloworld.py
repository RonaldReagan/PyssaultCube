#First we import all the tools we need. Because this is running in the example directory I have this extra code to make sure it can find the module.
#To import ACMap, you could just do: "from PyACube.mapfiles.cgz import ACMap" rather than all of the extra stuff I have written in here.
try:
	#First try to import from the main installed package
	from PyACube.mapfiles.cgz import ACMap
except ImportError:
	#Then assume we are in the examples folder.
	import sys; sys.path.insert(0, "..")
	from PyACube.mapfiles.cgz import ACMap

#A map generation script might look like this:
# * Create map, either by:
#     - Parsing a map and loading it into memory
#     - Creating a totally blank map and loading it into memory
#    In this case, we are loading a blank map
# * Edit map:
#     - Editing the header to include a map title, different waterlevel and ambient light.
#     - Modifying cubes
#     - Adding entities
# * Saving map:
#     - By ACMap.writeCGZ(mappath)
#     - Or if you loaded a preexisting map, you can do ACMap.save() and overwrite the previous map.

#This is the map that we will save. I like putting this up at the top so it is easy to modify.
mappath = "./results/ac_helloworld.cgz"

#Here we load up an empty map with these arguments:
# 'parse = False' - this indicates that we do not want to parse a map file, rather we want to make an empty one.
# 'sfactor = 6'   - as we are creating an empty map, we have to include the size. If you are loading up a map, this does nothing.
# 'maptitle = <title>' - this is the title of our map. Notice how you can use colors in this.
acmap = ACMap(parse = False, sfactor = 6, maptitle = "\f3Hello World!")

#Lets draw something on our map. Lets make every other cube raised up one and have a different texture.
for i, cube in enumerate(acmap.cubelist):

	#There is a couple ways to get x and y, here we do one.
	x,y = acmap.returnXY(i)
	
	#Now simple logic to see if we modify the cube.
	if x%2 == 0 and y%2 == 0:
		#Add one to the floor height
		cube.floor += 1
		#Change the floor texture to texture slot 10
		cube.ftex = 10

#Make sure the map isn't ugly.
acmap.drawBorder()
#Light our map up. Quick and dirty way to add light.
acmap.header.ambient = 100
#Lets remove our water from being visible.
acmap.header.waterlevel = -10

#As we created an empty map, we have to save using writeCGZ.
acmap.writeCGZ(mappath)
