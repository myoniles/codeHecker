# Intro

The CodeHecker is a project that I want to make my code, usable but only barely understandable.
This was an idea that I had ever since my first semester at Purdue and felt that its high time I pursue my dream of somehow making my code even less readable.

This project, at least in its early stages will focus only on C++ code. Once they types of C++ and object hecking has been added, I will expand to other file types.

# Current proposed workflow:

- take in code file
- Get file type to specify language-specific tokens
- traverse line by line and do the following:
	- remove lines with comments
	- add declared variables to variable list
	- replace variables names with their hashes
- write to new file: "{filename}_new.{type}"
- recompile
- if stderr is written to, abort
- else replace old file with new file

# Options

-h: help

-t: format of argument. if none are specified, it will check the file ending

-s: be silent

-f: replace even if there are compile errors after hecking up
