#!/usr/bin/env python3
import sys
import re
import hashlib
import getopt
import json

TYPE = ""
VARIABLE = {}


def detect_code_type(file_name):
	global TYPE
	file_name = file_name.split(".")
	if file_name[1]:
		TYPE = file_name[-1]
	return

def heck_split(line):
	delims = " ", "(", ")", ",", "+", "-", "/","*", "%", "\n", "="
	delims = '|'.join(map(re.escape, delims))
	line = re.split(str(delims) ,line)
	return line

def replace_variable(var_name):
	global VARIABLE
	VARIABLE.update({var_name:hashlib.sha1(var_name).hexdigest()})
	return

def check_for_dec(unded_str):
	unded_str.split("=")
	with open("types.json", "r") as fille:
		data = json.load(fille)
		print(data[TYPE])

def compile():
	return

def abort():
	return

def __main__():
	detect_code_type(sys.argv[1])
	fille = open(sys.argv[1], "r", encoding="utf-8")
	for l in fille:
		check_for_dec(l)
		l = heck_split(l)
	return

if __name__ == "__main__":
	__main__()
