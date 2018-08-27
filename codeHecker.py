#!/usr/bin/env python3

# Current proposed workflow:
# take in code file
# Get file type to specify lanague-specific tokens
# traverse line by line and do the following:
#		remove lines with comments
#		add declared variables to variable list
#		replace variables names with their hashes
# write to new file: "{filename}_new.{type}"
# recompile
# if stderr is written to, abort
# else replace old file with new file

# options:
# -h: help
# -f: format of argument. if none are specified, it will check the file ending
# -s: be silent
# -f: replace even if there are compile errors after hecking up

import sys
import hashlib
import getopt

def detect_code_type():
	return

def tokenize_line():
	return

def replace_variable():
	return

def compile():
	return

def abort():
	return

def __main__():
	return

if __name__ == "__main__":
	main()
