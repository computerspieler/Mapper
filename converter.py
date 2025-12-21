#!/usr/bin/env python3
# This script converts MCP mappings into Enigma mapping

import sys
import zipfile
import csv
import argparse

from config import *
from common import *

client_jar = None
server_jar = None

parser = argparse.ArgumentParser(
	prog="converter.py",
	description="Converts MCP version into Enigma parser"
)

parser.add_argument("mcp_archive")
parser.add_argument("-c", "--client", default="")
parser.add_argument("-s", "--server", default="")
parser.add_argument('-f', '--filtering',
	action='store_true',
	help="""This option will filter out every temporary names for fields or methods.
Useful for people trying to expand the list of methods and fields, not recommanded for modders""")
args = parser.parse_args()

if not args.server and not args.client:
	print("No minecraft clients, nor server have been provided, leaving")
	sys.exit(-1)

if args.client:
	client_jar = JarFile()
	client_jar.filtering = args.filtering
	print("Read the client JAR file")
	with zipfile.ZipFile(args.client, 'r') as archive:
		addSymbols(archive, client_jar)

if args.server:
	server_jar = JarFile()
	server_jar.filtering = args.filtering
	print("Read the server JAR file")
	with zipfile.ZipFile(args.server, 'r') as archive:
		addSymbols(archive, server_jar)

def addCSVToFilter(archive: zipfile.ZipFile, path: str,
	index_start_row: int,
	column_client_obfuscation: int,
	column_server_obfuscation: int,
	column_deobfuscated: int
):
	with archive.open(path) as csv_file:
		reader = csv.reader(map(
			lambda line: line.decode(),
			csv_file.read().splitlines()
		))
		for i in range(index_start_row):
			next(reader)
		for row in reader:
			if len(row) == 0:
				continue
			# If this is a name present in the client
			if row[column_client_obfuscation] != "*" and client_jar:
				client_jar.addToFilter(row[column_client_obfuscation], row[column_deobfuscated])
			# If this is a name present in the server
			if row[column_server_obfuscation] != "*" and server_jar:
				server_jar.addToFilter(row[column_server_obfuscation], row[column_deobfuscated])

# Parse the RGS file
def parse_names(name):
	return (name[:name.rfind('/')], name[name.rfind('/') + 1:])

def parse_line_rgs(line: str, jar):
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

def parse_line_srg(line: str, jar):
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

with zipfile.ZipFile(args.mcp_archive, 'r') as archive:
	for file_path in archive.namelist():
		filename = file_path[max(file_path.rfind('/'), file_path.rfind('\\'))+1:]
		
		if filename == "newids.csv":
			print("Read the new ids'")
			addCSVToFilter(archive, file_path,
				CSV_CLASS_START_ROW,
				CLIENT_OBF_NEWIDS_COL,
				SERVER_OBF_NEWIDS_COL,
				NON_OBF_NEWIDS_COL
			)

		if filename == "classes.csv":
			print("Read the classes' names")
			with archive.open(file_path) as csv_file:
				reader = csv.reader(map(
					lambda line: line.decode(),
					csv_file.read().splitlines()
				))
				for line, row in enumerate(reader):
					if line < CSV_CLASS_START_ROW:
						continue
					if len(row) == 0:
						continue
					# If this is a name present in the client
					if row[CLIENT_OBF_CLASS_COL] != "*" and client_jar:
						client_jar.setClassName(row[CLIENT_OBF_CLASS_COL], row[NON_OBF_CLASS_COL])
					# If this is a name present in the server
					if row[SERVER_OBF_CLASS_COL] != "*" and server_jar:
						server_jar.setClassName(row[SERVER_OBF_CLASS_COL], row[NON_OBF_CLASS_COL])

		if filename == "methods.csv":
			print("Read the methods' names")
			addCSVToFilter(archive, file_path,
				CSV_METHOD_START_ROW,
				CLIENT_OBF_METHOD_COL,
				SERVER_OBF_METHOD_COL,
				NON_OBF_METHOD_COL
			)

		if filename == "fields.csv":
			print("Read the fields' names")
			addCSVToFilter(archive, file_path,
				CSV_FIELD_START_ROW,
				CLIENT_OBF_FIELD_COL,
				SERVER_OBF_FIELD_COL,
				NON_OBF_FIELD_COL
			)

		if client_jar:
			if filename == "minecraft.rgs":
				print("Parse minecraft.rgs")
				with archive.open(file_path) as rgs_file:
					for line in rgs_file.read().splitlines():
						line = line.decode()
						try:
							parse_line_rgs(line, client_jar)
						except KeyError as e:
							print("Warning: The following line generated an exception")
							print(line)
			if filename == "minecraft.srg":
				print("Parse minecraft.srg")
				with archive.open(file_path) as srg_file:
					for line in srg_file.read().splitlines():
						line = line.decode()
						try:
							parse_line_srg(line, client_jar)
						except KeyError as e:
							print("Warning: The following line generated an exception")
							print(line)

		if server_jar:
			if filename == "minecraft_server.rgs":
				print("Parse minecraft_server.rgs")
				with archive.open(file_path) as rgs_file:
					for line in rgs_file.read().splitlines():
						line = line.decode()
						try:
							parse_line_rgs(line, server_jar)
						except KeyError as e:
							print("Warning: The following line generated an exception")
							print(line)
			if filename == "minecraft_server.srg":
				print("Parse minecraft_server.srg")
				with archive.open(file_path) as srg_file:
					for line in srg_file.read().splitlines():
						line = line.decode()
						try:
							parse_line_srg(line, server_jar)
						except KeyError as e:
							print("Warning: The following line generated an exception")
							print(line)

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
if client_jar:
	updateSignatures(client_jar)
if server_jar:
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
if client_jar:
	removeUselessEntries(client_jar)
if server_jar:
	removeUselessEntries(server_jar)

print("Move some classes into the default package")
def moveToDefaultPackage(jar):
	for c in jar.classes.copy():
		if jar.classes[c].getObfClassName().find('/') == -1:
			jar.classes[c].deobf_name = PACKAGE_DEFAULT + jar.classes[c].getDeobfClassName()
DEOBFUSCATED={
	"paulscode"
}

if client_jar:
	moveToDefaultPackage(client_jar)
if server_jar:
	moveToDefaultPackage(server_jar)

print("Write the mappings files")
if client_jar:
	with open("client.deobf", "w") as output:
		output.write(str(client_jar))

if server_jar:
	with open("server.deobf", "w") as output:
		output.write(str(server_jar))
