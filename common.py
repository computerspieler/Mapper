from config import *

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

# Read the jar files
# Necessary in order to get fields' signatures
from Krakatau.Krakatau.classfileformat.reader import Reader
from Krakatau.Krakatau.classfileformat.classdata import ClassData
from Krakatau.Krakatau.assembler.disassembly import Disassembler

import re
from io import StringIO

def readArchive(archive, name):
	with archive.open(name.decode('utf8')) as f:
		return f.read()

def addSymbols(archive, jar, already_deobf = False):
	for f in archive.namelist():
		if not f.endswith(".class"):
			continue
		
		f = f.encode('utf8')
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
			const_match = re.search(r"^\.const ([^ ]+) = (.*)$", line)
			class_match = re.search(r"^\.class.* ([^ ]+)$", line)
			field_match = re.search(r"^\.field.* ([^ ]+) ([^ ]+)", line)
			method_match = re.search(r"^\.method.* ([^ ]+) : ([^ ]+)", line)
			if class_match != None:
				classname = class_match.group(1)
				jar.addClass(classname)
				if already_deobf:
					jar.classes[classname].is_deobfuscated = True
				else:
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

