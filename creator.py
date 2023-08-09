# Copyright (C) 2022 Computerspieler
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import functools
import os.path
import time, zipfile, sys
import csv, re

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

import Krakatau.Krakatau
from Krakatau.Krakatau import script_util
from Krakatau.Krakatau.classfileformat.reader import Reader
from Krakatau.Krakatau.classfileformat.classdata import ClassData
from Krakatau.Krakatau.assembler.disassembly import Disassembler
from common import *

file_jar = JarFile()

print("Read the JAR file")
with zipfile.ZipFile(sys.argv[1], 'r') as archive:
	addSymbols(archive, file_jar, True)

print("Write the mapping file")
with open(sys.argv[2], "w") as output:
	output.write(str(file_jar))
