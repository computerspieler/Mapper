#!/usr/bin/env python3
# This script converts MCP mappings into Enigma mapping

# ==== CONFIGURATION ====
# Note: The first column's index is 0

# classes.csv configuration
CLIENT_OBF_CLASS_COL=2	# Column of the obfuscated name for the client jar
SERVER_OBF_CLASS_COL=4	# Column of the obfuscated name for the server jar
NON_OBF_CLASS_COL=0		# Column of the correct name
CSV_CLASS_START_ROW=4	# Number of rows to skip at the beginning

# methods.csv configuration
CLIENT_OBF_METHOD_COL=1	# Column of the obfuscated name for the client jar
SERVER_OBF_METHOD_COL=3	# Column of the obfuscated name for the server jar
NON_OBF_METHOD_COL=4	# Column of the correct name
CSV_METHOD_START_ROW=4	# Number of rows to skip at the beginning

# fields.csv configuration
CLIENT_OBF_FIELD_COL=2	# Column of the obfuscated name for the client jar
SERVER_OBF_FIELD_COL=5	# Column of the obfuscated name for the server jar
NON_OBF_FIELD_COL=6		# Column of the correct name
CSV_FIELD_START_ROW=3	# Number of rows to skip at the beginning

# newids.csv configuration
CLIENT_OBF_NEWIDS_COL=0	# Column of the obfuscated name for the client jar
SERVER_OBF_NEWIDS_COL=1	# Column of the obfuscated name for the server jar
NON_OBF_NEWIDS_COL=2	# Column of the correct name
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

# ==== END OF CONFIGURATION ====

import os.path
import zipfile
import csv

from common import *

client_jar = JarFile()
server_jar = JarFile()

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
	mclass_match = re.search(r"^\.class_map ([^ ]*) ([^ ]*)$", line)
	mfield_match = re.search(r"^\.field_map ([^ ]+) ([^ ]+)$", line)
	mmethod_match = re.search(r"^\.method_map ([^ ]+) ([^ ]+) ([^ ]+)$", line)

	class_match = re.search(r"^\.class ([^ ]+)$", line)
	field_match = re.search(r"^\.field ([^ ]+) ([^ ]+)$", line)
	method_match = re.search(r"^\.method ([^ ]+) ([^ ]+)$", line)
	
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
	class_match = re.search (r"^CL: ([^ ]+) ([^ ]+)$", line)
	field_match = re.search (r"^FD: ([^ ]+) ([^ ]+)$", line)
	method_match = re.search(r"^MD: ([^ ]+) ([^ ]+) ([^ ]+)", line)

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
