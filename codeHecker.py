#!/usr/bin/env python3
import sys
import re
import hashlib
import getopt

TYPE = ""
VARIABLE = {}


def detect_code_type(file_name):
	global TYPE
	file_name = file_name.split(".")
	if file_name[1]:
		TYPE = file_name[-1]
	return

def hash_variable(var_name):
	global VARIABLE
	if var_name not in VARIABLE:
		VARIABLE[varname] = var_name:hashlib.sha1(var_name).hexdigest()
	return

# magic for finding variable name: (\w+)(\[.*\])*\ *=
# however this doesn't find declarations like:
# 		int foo;
# that is matched by: (?:\w+\s+)([a-zA-Z_]\w*)
# the regex that does mathc to that doesn't handle python declarations,
# it is too limited in that it requires a word in front of it to be a variable

def check_for_var(unded_str):
	# values that have been declared equal to a value:
	#		darn = 1
	matches = re.findall(r'(\w+)(\[.*\])*\ *=', unded_str)
	# values that have simply been declared with a type
	# 	int heck = 1
	matches = matches +  re.findall(r'(?:\w+\s+)([a-cA-Z_]\w*)', unded_str)
	for var_name in matches:
		hash_variable(var_name)
	return

def compile():
	return

def abort():
	return

def __main__():
	detect_code_type(sys.argv[1])
	with open(sys.argc[1], "r") as unAlteredFile:
		inBlock = False
		for line in unAlteredFile:
			inBlock = remove_comments(line)
			check_for_var(line)

if __name__ == "__main__":
	__main__()
