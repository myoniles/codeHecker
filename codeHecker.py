#!/usr/bin/env python3
import sys
import re
import hashlib
from argparse import ArgumentParser
# we are using subprocess for better stderr checking
# This makes the program *very* dangerous
import subprocess

# as of now, this only supports two comment types, python / shell and C-style comments
C_COMMENT = True
VARIABLE = {}
COMP = ""

COMMENT = {"slashes":"//","block_start":"\\*", "block_end":"*/","hash_comment":"#"}

def getArgs():
	parser = ArgumentParser()
	parser.add_argument("file", help="The code file being hecked")
	parser.add_argument("-t","--type", help="specfiy the type of the file being hecked")
	parser.add_argument("-f","--force", action="store_true", help="replace the file even if there were problems in compilation")
	parser.add_argument("-v","--verbose", action="store_true", help="print to stdout")
	return parser.parse_args()

def detect_code_type(file_name):
	global TYPE
	global COMP
	uses_c = {"java":True,"c":True, "cpp":True, "sh":False, "py":False}
	# We use source for shell here to have an easier implementation
	# Also I am taking a guess on python3 RIP
	comp = {"java":"javac","c":"gcc", "cpp":"g++", "sh":"source", "py":"python3"}
	file_name = file_name.split(".")
	if file_name[1]:
		TYPE = uses_c[file_name[-1]]
		COMP = comp[file_name[-1]]
	return

def hash_variable(var_name):
	global VARIABLE
	if var_name not in VARIABLE:
		hashStr = hashlib.sha1(var_name.encode('utf-8')).hexdigest()
		# most langauges dont allow for variables to begin with a number
		newFirst = hashStr[0]
		if not hashStr[0].isalpha():
			newFirst = chr(int(hashStr[0]) + 97)
		VARIABLE[var_name] = newFirst + hashStr[1:]
	return

def remove_comments(line, in_block):
	global COMMENT
	global C_COMMENT

	# is the comment format python?
	if not C_COMMENT:
		line = line.split("#")[0]
		return line, False
	else:
		# I do a lot of checking here just make sure that a single
		# string is passed rather than a tuple
		if "//" in line:
			# we need to know if this is a whole line comment or a comment at the end
			line = line.split("//")
			if line[0].isspace() or line == "":
				return "", in_block
			else:
				line = line[0]
		# This one line on regex will deal with block comments in the middle of lines
		line = re.sub(r'/\*.*\*/', "", line)

		# I could do all blocks with multiline regex but I am afraid of unforseen consequences
		# such as not being able to see the whole document
		# re.sub(r'/\*.*?\*/', '', whole_gosh_darn_file, re.DOTALL)

		# is this the start of the block?
		if "/*" in line:
			line = line.split("/*")
			line = "".join(line[:-1])
		# is this the end of the block?
		if "*/" in line:
			line = line.split("*/")
			# if there is code written after the block, include that
			if line[1]:
				line = "".join(line[1:])
			in_block = False
		return (line, in_block)

# magic for finding variable name: (\w+)(\[.*\])*\ *=
# however this doesn't find declarations like:
# 		int foo;
# that is matched by: (?:\w+\s+)([a-zA-Z_]\w*)
# the regex that does mathc to that doesn't handle python declarations,
# it is too limited in that it requires a word in front of it to be a variable
def check_for_var(unded_str):
	# ignore references to variables inside of strings
	unded_str = re.sub(r'\".*?\"', '', unded_str)
	# values that have been declared equal to a value:
	#		darn = 1
	regexIsFun = re.findall(r'(\w+)(\[.*\])*\ *=', unded_str)
	# the above regex actually matches on two different components of the string
	# we only want the first
	regexIsFun = [entry[0] for entry in regexIsFun]
	# values that have simply been declared with a type
	# 	int heck
	regexIsFun = regexIsFun + re.findall(r'(?:\w+\**\s+)([A-Za-z_]\w*)', unded_str)
	if 'main' in regexIsFun:
		regexIsFun.remove('main') # this is important
	for var_name in regexIsFun:
		hash_variable(var_name)
	return

def remove_var(line):
	global VARIABLE
	# we will hold on to the first char, this will help maintain space / tab indentation
	for hashed_var in VARIABLE.keys():
		debug = r"(?<!\\)(\b)({}\b)".format(hashed_var)
		line = re.sub(debug, VARIABLE[hashed_var], line)
	return line

def abort(filename):
	try:
		# print("Problem encountered, preparing to abort")
		# this is the scariest line in my code
		subprocess.call(["rm", filename])
	except:
		#print("unable to remove files created, please do so manually")
		print("")
	quit()

def __main__():
	global COMP
	args = getArgs()
	filename = args.file
	file_desc = filename.split(".")
	detect_code_type(filename)
	hecked_name = file_desc[0] + "_hecked" + "."+ file_desc[1]
	with open(hecked_name, "w") as alteredFile:
		with open(filename, "r") as unAlteredFile:
			inBlock = False
			for line in unAlteredFile:
				line, inBlock = remove_comments(line, inBlock)
				check_for_var(line)
				line = remove_var(line)
				if(args.verbose):
					print(line)
				else:
					alteredFile.write(line)

		# At this point in the code, file_hecked.type has been written
		# Lets pass it to out compiler / interpreter
	try:
		return_code = subprocess.call([COMP, hecked_name])
		if return_code and not args.force:
			abort(hecked_name)

		# just rename the file, recompilation is not necessary
		subprocess.call(["mv",hecked_name, filename])
		return
	except:
		if not args.force:
			abort(hecked_name)
		return

if __name__ == "__main__":
	__main__()
