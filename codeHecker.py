#!/usr/bin/env python3
import sys
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

def tokenize_line():
	return

def replace_variable():
	hashlib.md5()
	return

def compile():
	return

def abort():
	return

def __main__():
	detect_code_type(sys.argv[1])
	print(TYPE)
	return

if __name__ == "__main__":
	__main__()
