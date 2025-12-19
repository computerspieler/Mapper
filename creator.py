#!/usr/bin/env python3
# This script creats mapping files of JAR files

import argparse
import zipfile
import re

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

from Krakatau.Krakatau.classfileformat.reader import Reader
from Krakatau.Krakatau.classfileformat.classdata import ClassData
from Krakatau.Krakatau.assembler.disassembly import Disassembler
from common import *

file_jar = JarFile()

parser = argparse.ArgumentParser(
	prog = "creator.py",
	description = "Create symbol mapping of JAR files"
)

parser.add_argument('jar_file')
parser.add_argument('output_file')

args = parser.parse_args()

print("Read the JAR file")
with zipfile.ZipFile(args.jar_file, 'r') as archive:
	addSymbols(archive, file_jar, True)

print("Write the mapping file")
with open(args.output_file, "w") as output:
	output.write(str(file_jar))
