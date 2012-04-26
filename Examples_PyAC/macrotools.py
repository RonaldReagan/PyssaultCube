#!/usr/bin/env python
# Easily create and view macros in the shell
# Note that macros appear vertically stretched, as the shell chars are not square
# This file is mostly written by Lantry, but has some minor adjustments by RR.

def viewMacro(m):
	"""
		prints a visual representation of the given macro
	"""
	height = max([coord[1] for coord in m]) + 1
	width = max([coord[0] for coord in m]) + 1
	result = [ ' ' * width ] * height
	for coord in m:
		result[coord[1]] = result[coord[1]][:coord[0]] + 'x' + result[coord[1]][coord[0] + 1:]
	for line in result:
		print(line)

def createMacro():
	"""
		converts user input into a string representing a macro
		Enter the macro line by line, type 'stop' or 'done' when finished
	"""
	result = []
	lineNum = 0
	while True:
		line = raw_input('Enter next line: ').lower()
		if line in ['done', 'stop', 'd', 's']:
			break
		else:
			for i in range(len(line)):
				if line[i] == 'x':
					result += [[i, lineNum]]
				elif line[i] == '\n':
					lineNum += 1
			lineNum += 1
	return str(result).replace(' ', '')
	
	
if __name__ == "__main__":
	print createMacro()