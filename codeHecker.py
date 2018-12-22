#!/usr/bin/env python3
import sys
import re
import hashlib
from argparse import ArgumentParser

TYPE = ""
VARIABLE = {}

COMMENT = {"block_start":"\\*", "block_end":"*/","hash_comment":"#"}

def getArgs():
	parser = ArgumentParser()
	parser.add_argument("file", help="The code file being hecked")
	parser.add_argument("-t","--type", help="specfiy the type of the file being hecked")
	parser.add_argument("-f","--force", help="replace the file even if there were problems in compilation")
	parser.add_argument("-v","--verbose", help="print to stdout")
	return parser.parse_args()

def detect_code_type(file_name):
	global TYPE
	file_name = file_name.split(".")
	if file_name[1]:
		TYPE = file_name[-1]
	return

def hash_variable(var_name):
	global VARIABLE
	if var_name not in VARIABLE:
		VARIABLE[var_name] = hashlib.sha1(var_name.encode('utf-8')).hexdigest()
	return

def remove_comments(uned_str, in_block):
	global COMMENT
	global TYPE
	# ignore comments inside of strings
	# yes I know its unlikely but still
	if COMMENT["block_end"] in uned_str:
		uned_str.split(COMMENT["block_end"])
		# if there is code written after the block, include that
		if unedstr[1]:
			uned_str = unedstr[1]
		in_block = False
	return (uned_str, in_block)

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
	args = getArgs()
	filename = args.file
	detect_code_type(filename)
	with open(filename, "r") as unAlteredFile:
		inBlock = False
		for line in unAlteredFile:
			line, inBlock = remove_comments(line, inBlock)
			check_for_var(line)

if __name__ == "__main__":
	__main__()
