from structio import *

#And lets hope the maps use the most recent version 6. Lazy version bumping happened back in 93 days...
HEADER_6 = [
			{	
				"name":"head",
				"len": 4,
				"type":TYPE_STR,
				"_unused_": True
			},
			{	
				"name":"version",
				"type":TYPE_INT,
				"_unused_": True
			},
			{	
				"name":"headersize",
				"type":TYPE_INT
			},
			{	"name":"sfactor",
				"len":4,
				"type":TYPE_INT
			},
			{	"name":"numents",
				"type":TYPE_INT
			},
			{	"name":"maptitle",
				"len":128,
				"type":TYPE_STR
			},
			{	"name":"texlistA",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"texlistB",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"texlistC",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"waterlevel",
				"type":TYPE_INT
			},
			{	"name":"watercolorR",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorG",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorB",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorA",
				"type":TYPE_UCHAR
			},
			{	"name":"reserved",
				"len": 14,
				"type":TYPE_INTLIST
			},
			]

#Version bump @r4657, Never in a release?		
HEADER_7 = [
			{	
				"name":"head",
				"len": 4,
				"type":TYPE_STR,
				"_unused_": True
			},
			{	
				"name":"version",
				"type":TYPE_INT,
				"_unused_": True
			},
			{	
				"name":"headersize",
				"type":TYPE_INT
			},
			{	"name":"sfactor",
				"len":4,
				"type":TYPE_INT
			},
			{	"name":"numents",
				"type":TYPE_INT
			},
			{	"name":"maptitle",
				"len":128,
				"type":TYPE_STR
			},
			{	"name":"texlistA",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"texlistB",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"texlistC",
				"len":256,
				"type":TYPE_UCHARLIST
			},
			{	"name":"waterlevel",
				"type":TYPE_INT
			},
			{	"name":"watercolorR",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorG",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorB",
				"type":TYPE_UCHAR
			},
			{	"name":"watercolorA",
				"type":TYPE_UCHAR
			},
			{	"name":"maprevision",
				"type":TYPE_INT
			},
			{	"name":"ambient",
				"type":TYPE_INT
			},
			{	"name":"reserved",
				"len": 12,
				"type":TYPE_INTLIST
			},
			{	"name":"mediareq",
				"len": 128,
				"type":TYPE_STR
			}
			]

#Version bump @r4899
HEADER_8 = HEADER_7 #Same as ver 7

#Version bump @r7382
HEADER_9 = HEADER_8[:-1] #Same as ver 8, but w/o mediapacks

#Use to get the correct header for the version.
Headers = {6:HEADER_6, 7:HEADER_7, 8:HEADER_8, 9:HEADER_9} 
			
ENTITY = [
			{	
				"name":"x",
				"type":TYPE_SHORT
			},
			{	
				"name":"y",
				"type":TYPE_SHORT
			},
			{	
				"name":"z",
				"type":TYPE_SHORT
			},
			{	
				"name":"attr1",
				"type":TYPE_SHORT
			},
			{	
				"name":"kind",
				"type":TYPE_UCHAR
			},
			{	
				"name":"attr2",
				"type":TYPE_UCHAR
			},
			{	
				"name":"attr3",
				"type":TYPE_UCHAR
			},
			{	
				"name":"attr4",
				"type":TYPE_UCHAR
			}
		]

SQUARE = [
			{	
				"name":"kind",
				"type":TYPE_UCHAR,
				"_unused_":True
			},
			{	
				"name":"floor",
				"type":TYPE_CHAR,
				"default": 0,
				"_spaceonly_": True
			},
			{	
				"name":"ceil",
				"type":TYPE_CHAR,
				"default": 16,
				"_spaceonly_": True
			},
			{	
				"name":"wtex",
				"type":TYPE_UCHAR
			},
			{	
				"name":"ftex",
				"type":TYPE_UCHAR,
				"default": 3,
				"_spaceonly_": True
			},
			{	
				"name":"ctex",
				"type":TYPE_UCHAR,
				"default": 5,
				"_spaceonly_": True
			},
			{	
				"name":"vdelta",
				"type":TYPE_UCHAR
			},
			{	
				"name":"utex",
				"type":TYPE_UCHAR,
				"default": 2,
				"_spaceonly_": True
			},
			{	
				"name":"tag",
				"type":TYPE_UCHAR,
				"default": 0,
				"_spaceonly_": True
			}
		]
