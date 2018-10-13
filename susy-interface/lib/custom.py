class Collection():
	def __init__(self, path):
		self.path = path
		self.objs = []
		self.parse()
	def parse(self):
		lines    = [l.rstrip("\n").strip() for l in open(self.path, "r").readlines()]
		obj      = ""
		consumed = False
		parsed   = []
		for line in lines:
			if len(line) == 0: continue
			if line[0:1] == "#": continue
			if line.find("BEGIN") > -1:
				tag = line.split("::")[1]
				obj = Custom(tag)
				continue
			elif line == "ENDDEF":
				self.objs.append(obj)
				tag    = ""
				obj    = None
				parsed = []
				continue
			elif tag != "":
				if line.find(":=") == -1: continue
				sl = [s.strip() for s in line.split(":=")]
				if   sl[0]     == "name": continue
				if   sl[0][-1] == "+": parsed = self.parseAppend (obj, sl, consumed, parsed)
				elif sl[0][-1] == "#": parsed = self.parseSpecial(obj, sl, consumed, parsed)
				elif sl[0].strip() == "consume": 
					others = [o.name for o in self.objs]
					if not sl[1] in others: continue
					self.objs[others.index(sl[1])].copy(obj)
					consumed = True
				else: setattr(obj, sl[0], sl[1]); parsed.append(sl[0])
	def parseAppend(self, obj, sl, reset=False, parsed=[]):
		sl[0] = sl[0].rstrip("+").strip()
		vals  = [s.strip() for s in sl[1].split(";")]
		if hasattr(obj, sl[0]) and (not reset or sl[0] in parsed): getattr(obj, sl[0]).extend(vals)
		else: setattr(obj, sl[0], vals)
		if not sl[0] in parsed: parsed.append(sl[0])
		return parsed
	def parseSpecial(self, obj, sl, reset=False, parsed = []):
		sl[0] = sl[0].rstrip("#").strip()
		fullline = sl[1].strip("{").strip("}")
		key = fullline.split(":")[0].strip()
		val = fullline.split(":")[1].strip().split(";")
		if hasattr(obj, sl[0]) and (not reset or sl[0] in parsed): getattr(obj, sl[0])[key] = [v.strip() for v in val]
		else: setattr(obj, sl[0], {key:[v.strip() for v in val]})
		if not sl[0] in parsed: parsed.append(sl[0])
		return parsed
	def get(self, tag):
		thelist = [o.name for o in self.objs]
		if not tag in thelist: raise RuntimeError, "Object '" + tag + "' does not exist in collection '" + self.path + "'"
		return self.objs[thelist.index(tag)]
	def getAllNames(self):
		return [o.name for o in self.obj]

class Custom():
	def __init__(self, name):
		self.name = name
	def copy(self, newobj):
		for attr in self.__dict__.keys():
			if attr=="name": continue
			setattr(newobj, attr, getattr(self, attr))

