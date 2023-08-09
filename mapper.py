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

class Method:
	def __init__(self, obf_name, signature):
		self.obf_name = obf_name
		self.deobf_name = None
		self.signature = signature
		self.hasBeenRenamed = False

	def setDeobfuscatedName(self, deobf_name):
		self.deobf_name = deobf_name
		self.hasBeenRenamed = True
	
	def getObfClassName(self):
		return self.obf_name

	def getDeobfClassName(self):
		if self.deobf_name is None:
			return self.getObfClassName()
		else:
			return self.deobf_name
	
	def __str__(self):
		return "\tMETHOD {} {} {}\n".format(self.getObfClassName(), self.getDeobfClassName(), self.signature)

class Field:
	def __init__(self, obf_name, signature):
		self.obf_name = obf_name
		self.deobf_name = None
		self.signature = signature
		self.hasBeenRenamed = False

	def setDeobfuscatedName(self, deobf_name):
		self.deobf_name = deobf_name
		self.hasBeenRenamed = True
	
	def getObfClassName(self):
		return self.obf_name

	def getDeobfClassName(self):
		if self.deobf_name is None:
			return self.getObfClassName()
		else:
			return self.deobf_name
	
	def __str__(self):
		return "\tFIELD {} {} {}\n".format(self.getObfClassName(), self.getDeobfClassName(), self.signature)

class Class:
	def __init__(self, obf_name):
		self.obf_name = obf_name
		self.deobf_name = None
		self.hasBeenRenamed = False
		self.is_deobfuscated = False
		self.fields = {}
		self.methods = {}

	def getObfClassName(self):
		return self.obf_name
	
	def setDeobfuscatedName(self, deobf_name):
		self.deobf_name = deobf_name
		self.hasBeenRenamed = True

	def addField(self, obf, signature):
		self.fields[obf] = Field(obf, signature)

	def setFieldName(self, obf, deobf):
		self.fields[obf].setDeobfuscatedName(deobf)

	def setFieldSignature(self, obf, signature):
		self.fields[obf].signature = signature

	def addMethod(self, obf, signature):
		self.methods[(obf, signature)] = Method(obf, signature)

	def setMethodName(self, obf, signature, deobf):
		if not (obf, signature) in self.methods:
			self.addMethod(obf, signature)
			print("{}({}) => {}".format(obf, signature, deobf))
		self.methods[(obf, signature)].setDeobfuscatedName(deobf)

	def setMethodSignature(self, obf, old_signature, signature):
		self.methods[(obf, old_signature)].signature = signature

	def getDeobfClassName(self):
		if self.deobf_name is None:
			return self.getObfClassName()
		else:
			return self.deobf_name

	def __str__(self):
		output = "CLASS {} {}\n".format(self.getObfClassName(), self.getDeobfClassName())
		for obf in self.fields:
			output += self.fields[obf].__str__()

		for (obf, signature) in self.methods:
			output += self.methods[(obf, signature)].__str__()
		
		return output

class JarFile:
	def __init__(self):
		self.classes = {}
		self.filter = {}
		self.const = {}
		self.filtering = False

	def addClass(self, obf):
		if not obf in self.classes:
			self.classes[obf] = Class(obf)

	def setClassName(self, obf, deobf):
		self.classes[obf].setDeobfuscatedName(deobf)

	def setClassAsDeobfucated(self, obf, deobf):
		self.classes[obf].is_deobfuscated = True

	def addField(self, classname, obf, signature):
		self.classes[classname].addField(obf, signature)

	def setFieldName(self, classname, obf, deobf):
		if deobf in self.filter:
			deobf = self.filter[deobf]
		elif self.filtering:
			return
		
		self.classes[classname].setFieldName(obf, deobf)

	def setFieldSignature(self, classname, obf, signature):
		self.classes[classname].setFieldSignature(obf, signature)

	def addMethod(self, classname, obf, signature):
		self.classes[classname].addMethod(obf, signature)

	def setMethodName(self, classname, obf, signature, deobf):
		if deobf in self.filter:
			deobf = self.filter[deobf]
		elif self.filtering:
			return
		
		self.classes[classname].setMethodName(obf, signature, deobf)

	def setMethodSignature(self, classname, obf, old_signature, signature):
		self.classes[classname].setMethodSignature(obf, old_signature, signature)

	def addToFilter(self, name, replacement):
		self.filter[name] = replacement

	def __str__(self):
		output = ""
		for obf in self.classes:
			output += self.classes[obf].__str__()
		return output

client_jar = JarFile()
server_jar = JarFile()

# ==== CONFIGURATION ====
# Note: The first column's index is 0

# classes.csv configuration
CLIENT_OBF_CLASS_COL=2	# Collumn of the obfuscated name for the client jar
SERVER_OBF_CLASS_COL=4	# Collumn of the obfuscated name for the server jar
NON_OBF_CLASS_COL=0		# Collumn of the correct name
CSV_CLASS_START_ROW=4	# Number of rows to skip at the beginning

# methods.csv configuration
CLIENT_OBF_METHOD_COL=1	# Collumn of the obfuscated name for the client jar
SERVER_OBF_METHOD_COL=3	# Collumn of the obfuscated name for the server jar
NON_OBF_METHOD_COL=4	# Collumn of the correct name
CSV_METHOD_START_ROW=4	# Number of rows to skip at the beginning

# fields.csv configuration
CLIENT_OBF_FIELD_COL=2	# Collumn of the obfuscated name for the client jar
SERVER_OBF_FIELD_COL=5	# Collumn of the obfuscated name for the server jar
NON_OBF_FIELD_COL=6		# Collumn of the correct name
CSV_FIELD_START_ROW=3	# Number of rows to skip at the beginning

# newids.csv configuration
CLIENT_OBF_NEWIDS_COL=0	# Collumn of the obfuscated name for the client jar
SERVER_OBF_NEWIDS_COL=1	# Collumn of the obfuscated name for the server jar
NON_OBF_NEWIDS_COL=2	# Collumn of the correct name
CSV_NEWIDS_START_ROW=0	# Number of rows to skip at the beginning

PACKAGE_DEFAULT="net/minecraft/src/"
PACKAGE_CONSIDERED_DEOBFUSCATED=[
	"paulscode",
	"com/jcraft/jorbis",
]

# Filtering will filter out every function without a proper name
# Useful for people trying to expand the list of methods and fields
# Not recommanded for modders
client_jar.filtering = True
server_jar.filtering = True

# Read the jar files
# Necessary in order to get fields' signatures
def readArchive(archive, name):
    with archive.open(name.decode('utf8')) as f:
        return f.read()

def addSymbols(archive, jar):
	for f in [name.encode('utf8') for name in archive.namelist() if name.endswith(".class")]:
		data = readArchive(archive, f)
		# Warning! Skipping the file since it is not a valid classfile.
		if not data.startswith(b'\xca\xfe\xba\xbe'):
			print("{} is not a proper class file".format(f))
			continue
		clsdata = ClassData(Reader(data))
		buf = StringIO()
		Disassembler(clsdata, buf.write, roundtrip=False).disassemble()

		buf.seek(0)
		classname = None
		for line in buf:
			line = line.encode('utf-8').decode('utf-8')
			if len(line) <= 2: continue
			while line[-1] == '\n': line = line[:-1]
			while line[-1] == ' ' or line[-1] == '\t': line = line[:-1]
			const_match = re.search("^\\.const ([\[\]a-zA-Z0-9]+) = (.*)$", line)
			class_match = re.search("^\\.class.* ([a-zA-Z0-9/$_]+)$", line)
			field_match = re.search("^\\.field.* ([a-zA-Z0-9_]+) ([a-zA-Z0-9()\[\]/;]+)", line)
			method_match = re.search("^\\.method.* ([a-zA-Z0-9_/<>$]+) : ([a-zA-Z0-9()\[\]/$;]+)", line)
			if class_match != None:
				classname = class_match.group(1)
				jar.addClass(classname)
				for s in PACKAGE_CONSIDERED_DEOBFUSCATED:
					if classname.startswith(s):
						jar.classes[classname].is_deobfuscated = True
						break
			elif method_match != None:
				jar.addMethod(classname, method_match.group(1), method_match.group(2))
			elif field_match != None:
				jar.addField(classname, field_match.group(1), field_match.group(2))
			elif const_match != None:
				jar.const[const_match.group(1)] = const_match.group(2)

# Start
print("Read the client JAR file")
with zipfile.ZipFile("minecraft.jar", 'r') as archive:
	addSymbols(archive, client_jar)

print("Read the server JAR file")
with zipfile.ZipFile("minecraft_server.jar", 'r') as archive:
	addSymbols(archive, server_jar)

if os.path.exists("newids.csv"):
	print("Read the new ids'")
	with open("newids.csv", "r") as csv_file:
		reader = csv.reader(csv_file)
		for i in range(CSV_NEWIDS_START_ROW):
			next(csv_file)
		for row in reader:
			if len(row) == 0:
				continue
			# If this is a name present in the client
			if row[CLIENT_OBF_NEWIDS_COL] != "*":
				client_jar.addToFilter(row[CLIENT_OBF_NEWIDS_COL], row[NON_OBF_NEWIDS_COL])
			# If this is a name present in the server
			if row[SERVER_OBF_NEWIDS_COL] != "*":
				server_jar.addToFilter(row[SERVER_OBF_NEWIDS_COL], row[NON_OBF_NEWIDS_COL])

		csv_file.close()

if os.path.exists("classes.csv"):
	print("Read the classes' names")
	with open("classes.csv", "r") as csv_file:
		reader = csv.reader(csv_file)
		for i in range(CSV_CLASS_START_ROW):
			next(csv_file)
		for row in reader:
			if len(row) == 0:
				continue
			# If this is a name present in the client
			if row[CLIENT_OBF_CLASS_COL] != "*":
				client_jar.setClassName(row[CLIENT_OBF_CLASS_COL], row[NON_OBF_CLASS_COL])
			# If this is a name present in the server
			if row[SERVER_OBF_CLASS_COL] != "*":
				server_jar.setClassName(row[SERVER_OBF_CLASS_COL], row[NON_OBF_CLASS_COL])

		csv_file.close()

if os.path.exists("methods.csv"):
	print("Read the methods' names")
	with open("methods.csv", "r") as csv_file:
		reader = csv.reader(csv_file)
		for i in range(CSV_METHOD_START_ROW):
			next(csv_file)
		for row in reader:
			if len(row) == 0:
				continue
			# If this is a name present in the client
			if row[CLIENT_OBF_METHOD_COL] != "*":
				client_jar.addToFilter(row[CLIENT_OBF_METHOD_COL], row[NON_OBF_METHOD_COL])
			# If this is a name present in the server
			if row[SERVER_OBF_METHOD_COL] != "*":
				server_jar.addToFilter(row[SERVER_OBF_METHOD_COL], row[NON_OBF_METHOD_COL])

		csv_file.close()

if os.path.exists("fields.csv"):
	print("Read the fields' names")
	with open("fields.csv", "r") as csv_file:
		reader = csv.reader(csv_file)
		for i in range(CSV_FIELD_START_ROW):
			next(csv_file)
		for row in reader:
			if len(row) == 0:
				continue
			# If this is a name present in the client
			if row[CLIENT_OBF_FIELD_COL] != "*":
				client_jar.addToFilter(row[CLIENT_OBF_FIELD_COL], row[NON_OBF_FIELD_COL])
			# If this is a name present in the server
			if row[SERVER_OBF_FIELD_COL] != "*":
				server_jar.addToFilter(row[SERVER_OBF_FIELD_COL], row[NON_OBF_FIELD_COL])

		csv_file.close()

# Parse the RGS file
def parse_names(name):
	return (name[:name.rfind('/')], name[name.rfind('/') + 1:])

def parse_line_rgs(line, jar):
	mclass_match = re.search("^\\.class_map ([a-zA-Z][a-zA-Z0-9_/]*) ([a-zA-Z][a-zA-Z0-9_/]*)$", line)
	mfield_match = re.search("^\\.field_map ([a-zA-Z0-9_/$]+) ([a-zA-Z0-9_]+)$", line)
	mmethod_match = re.search("^\\.method_map ([a-zA-Z0-9_/$]+) ([a-zA-Z0-9()\[\]/;]+) ([a-zA-Z0-9_]+)$", line)

	class_match = re.search("^\\.class ([a-zA-Z][a-zA-Z0-9_/]*)$", line)
	field_match = re.search("^\\.field ([a-zA-Z0-9_/]+) ([a-zA-Z0-9()\[\]/;]+)$", line)
	method_match = re.search("^\\.method ([a-zA-Z0-9_/]+) ([a-zA-Z0-9()\[\]/;]+)$", line)
	
	if mclass_match is not None:
		jar.setClassName(mclass_match.group(1), mclass_match.group(2))
	elif mfield_match is not None:
		deobf_name = mfield_match.group(2)
		classname, name = parse_names(mfield_match.group(1))
		jar.setFieldName(classname, name, deobf_name)
	elif mmethod_match is not None:
		deobf_name = mmethod_match.group(3)
		signature = mmethod_match.group(2)
		classname, name = parse_names(mmethod_match.group(1))
		jar.setMethodName(classname, name, signature, deobf_name)
	elif class_match is not None:
		jar.setClassName(class_match.group(1), class_match.group(1))
	elif field_match is not None:
		classname, name = parse_names(field_match.group(1))
		signature = field_match.group(2)
		jar.setFieldName(classname, name, name)
	elif method_match is not None:
		classname, name = parse_names(method_match.group(1))
		signature = method_match.group(2)
		jar.setMethodName(classname, name, signature, name)

def parse_line_srg(line, jar):
	class_match = re.search ("^CL: ([a-zA-Z][a-zA-Z0-9_/]*) ([a-zA-Z][a-zA-Z0-9_/]*)$", line)
	field_match = re.search ("^FD: ([a-zA-Z0-9_/]+) ([a-zA-Z0-9()\[\]/;]+)$", line)
	method_match = re.search("^MD: ([a-zA-Z0-9_/]+) ([a-zA-Z0-9()\[\]/;]+) ([a-zA-Z0-9_/]+)", line)

	if class_match is not None:
		jar.setClassName(class_match.group(1), class_match.group(2))
	elif field_match is not None:
		deobf_name = field_match.group(2)
		classname, name = parse_names(field_match.group(1))
		jar.setFieldName(classname, name, deobf_name)
	elif method_match is not None:
		signature = method_match.group(2)
		classname, name = parse_names(method_match.group(1))
		_, deobf_name = parse_names(method_match.group(3))
		jar.setMethodName(classname, name, signature, deobf_name)

if os.path.exists("minecraft.rgs"):
	print("Parse minecraft.rgs")
	with open("minecraft.rgs") as rgs_file:
		for line in rgs_file:
			parse_line_rgs(line, client_jar)
if os.path.exists("minecraft.srg"):
	print("Parse minecraft.srg")
	with open("minecraft.srg") as srg_file:
		for line in srg_file:
			parse_line_srg(line, client_jar)

if os.path.exists("minecraft_server.rgs"):
	print("Parse minecraft_server.rgs")
	with open("minecraft_server.rgs") as rgs_file:
		for line in rgs_file:
			parse_line_rgs(line, server_jar)
if os.path.exists("minecraft_server.srg"):
	print("Parse minecraft_server.srg")
	with open("minecraft_server.srg") as srg_file:
		for line in srg_file:
			parse_line_srg(line, server_jar)

# Update the signatures
# Every classes which isn't in a package needs to be put in
# the "none" package, otherwise Enigma won't be happy
def updateSign(jar, sign):
	if sign in jar.const:
		m = re.search(r"Utf8 (.*)", jar.const[sign])
		if m != None:
			sign = m.group(1)
	return sign

def updateSignatures(jar):
	for c in jar.classes:
		for of in jar.classes[c].fields:
			f = jar.classes[c].fields[of]
			jar.setFieldSignature(c, of, updateSign(jar, f.signature))

		methods = jar.classes[c].methods.copy()
		for (om, signature) in methods:
			jar.setMethodSignature(c, om, signature, updateSign(jar, signature))

print("Update signatures")
updateSignatures(client_jar)
updateSignatures(server_jar)

# Clean the map from unupdated 
def removeUselessEntries(jar):
	for c in jar.classes.copy():
		if jar.classes[c].is_deobfuscated:
			continue
				
		fields = jar.classes[c].fields.copy()
		for of in fields:
			if not jar.classes[c].fields[of].hasBeenRenamed:
				jar.classes[c].fields.pop(of)
			
		methods = jar.classes[c].methods.copy()
		for (om, signature) in methods:
			if not jar.classes[c].methods[(om, signature)].hasBeenRenamed:
				jar.classes[c].methods.pop((om, signature))
		
		if not jar.classes[c].hasBeenRenamed and len(jar.classes[c].methods) == 0 and len(jar.classes[c].fields) == 0:
			jar.classes.pop(c)

print("Clean the map")
removeUselessEntries(client_jar)
removeUselessEntries(server_jar)

print("Move some classes into the default package")
def moveToDefaultPackage(jar):
	for c in jar.classes.copy():
		if jar.classes[c].getObfClassName().find('/') == -1:
			jar.classes[c].deobf_name = PACKAGE_DEFAULT + jar.classes[c].getDeobfClassName()
DEOBFUSCATED={
	"paulscode"
}
moveToDefaultPackage(client_jar)
moveToDefaultPackage(server_jar)

print("Write the mappings files")
with open("client.deobf", "w") as output:
	output.write(str(client_jar))

with open("server.deobf", "w") as output:
	output.write(str(server_jar))
