PyssaltCube
===========

Provides python utilities to AssaultCube written by Ronald_Reagan

List of contents:
-----------------
**PyACube**:
A python module for interacting with AssaultCube in various ways. Currently just reading, editing, and writing map files (cgz and cfg).
* mapfiles/ - submodule for interacting with cgz and cfg files
** cfg.py - defines classes and functions for reading and writing .cfg files. Main class is MapCFG.
** cgz.py - defines classes and functions for reading and writing .cfg files. Main class is ACMap.
** consts.py - defines constant values. This includes team numbers, currentmapformat (the currently supported map file format), cubetypes and such.
** misc.py - contains random utilities that may be used.

**Examples_PyACube**:
A directory containg files using PyACube.
* ac_random.py - a almost completely random map generator. The map is fully playable, however probably will not provide too much gameplay value. Demonstrates basic usage of the cgz module.
* mapcfgclean.py - cleans out all unused textures, mapmodels, and sounds from a maps config file. Demonstrates useage of both the cgz and cfg modules.
