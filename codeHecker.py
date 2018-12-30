#!/usr/bin/env python3
import sys
import re
import hashlib
from argparse import ArgumentParser

# as of now, this only supports two comment types, python / shell and C-style comments
C_COMMENT = True
VARIABLE = {}

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
	uses_c = {"java":True,"c":True, "cpp":True, "sh":False, "py":False}
	file_name = file_name.split(".")
	if file_name[1]:
		TYPE = uses_c[file_name[-1]]
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
	# 	int heck = 1
	regexIsFun = regexIsFun + re.findall(r'(?:\w+\s+)([a-cA-Z_]\w*)', unded_str)
	for var_name in regexIsFun:
		hash_variable(var_name)
	return

def remove_var(line):
	global VARIABLE
	# we will hold on to the first char, this will help maintain space / tab indentation
	first_char = ''
	if line:
		first_char = line[0]
	pattern = re.compile(r"\s") # OwO a new method for regex
	line = pattern.split(line)
	for word in range(len(line)):
		if line[word] == '':
			line[word] = first_char
		elif line[word] in VARIABLE:
			line[word] = VARIABLE[line[word]]
	line = " ".join(line)
	return line

def compile():
	return

def abort():
	return

def __main__():
	args = getArgs()
	filename = args.file
	detect_code_type(filename)
	with open(filename, "r") as unAlteredFile:
		inBlock = False
		for line in unAlteredFile:
			line, inBlock = remove_comments(line, inBlock)
			check_for_var(line)
			line = remove_var(line)
			if(args.verbose):
				print(line)

if __name__ == "__main__":
	__main__()
