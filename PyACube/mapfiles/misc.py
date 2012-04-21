def delAllEnts(mapf, enttype):
	"""
	mapf - a map file (class ACMap)
	enttype - Delete all ents of that type (int)
	"""
	i = 0
	while True:
		if i >= len(mapf.entities):
			break
		if mapf.entities[i].kind == enttype:
			del mapf.entities[i]
			mapf.header.numents -= 1
			continue
		i += 1

def printEnts(mapf):
	"""
	Goes through the map file and prints out all the entities
	"""
	formatstr = "Entity {0}: x-{1} y-{2} z-{3} attr1-{4} type-{5} attr2-{6} attr3-{7} attr4-{8}"
	for i in range(len(mapf.entities)):
		j = mapf.entities[i]
		print formatstr.format(i, j.xyz[0], j.xyz[1], j.xyz[2], j.attrs[0], j.kind, j.attrs[1], j.attrs[2], j.attrs[3])