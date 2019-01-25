import sqlite3, re, unittest, sys

class ScriptReader():
	"""Scans scripts for rules and keywords, which are then stored in a db"""
	def __init__(self, script):
		self.conn = sqlite3.connect('testdb')
		self.name = script
		self.create_script(self.name)		
		self.compile_re()
		self.scan_file(self.name)
	
	def create_script(self, name):
		if not self.already_exists('SCRIPT', name):
			self.conn.execute('INSERT INTO SCRIPT VALUES("' + self.name + '")')
			self.conn.commit()

	def scan_file(self, script):
		with open(script) as f:
			start = False
			for line in f:
				line = line.strip()
				if self.get_opening(line) and start == False:
					start = True
				else:
					if self.get_keyword(line):
						pass
					elif self.get_decomposition_rule(line):
						pass
					elif self.get_reassembly_rule(line):
						pass
					elif self.get_substitution_rule(line):
						pass
					elif self.get_equivalence_class(line):
						pass
			self.conn.close()
			print('Finished scanning.')

	def get_opening(self, line):
		try:
			temp = re.search(self.st, line).group
		except AttributeError as e:
			temp = None
		if temp:
			#res = self.clean_group(temp)
			if not self.already_exists('OPENING', temp(1)):
				try:
					self.conn.execute('INSERT INTO OPENING VALUES("' + temp(1) +'", "' + self.name + '")')
					self.conn.commit()
					return True
				except IndexError as e:
					pass

	def get_keyword(self, line):
		try:
			temp = re.search(self.kw, line).group
		except AttributeError as e:
			temp = None
		if temp:
			res = self.clean_group(temp)
			if not self.already_exists('KEYWORD', res[0].lower()):
				try:
					self.current_keyword = res[0].lower()
					rank = res[1]
				except IndexError as e:
					rank = 0
				try:
					self.current_eq = res[2].lower()
				except IndexError as e:
					self.current_eq = self.current_keyword
				self.conn.execute('INSERT INTO KEYWORD VALUES("' + self.current_keyword + '", ' + rank + ', "' + \
					self.current_eq + '", "' + self.name + '")')
				self.conn.commit()
				return True

	def get_decomposition_rule(self, line):
		try:
			temp = re.search(self.dr, line).group
		except AttributeError as e:
			temp = None
		if temp:
			if not self.already_exists('DECOMP_RULE', temp(1).lower()):
				self.current_d_rule = temp(1)
				self.conn.execute('INSERT INTO DECOMP_RULE VALUES("' + temp(1).lower() + '", "' + self.current_eq + \
					'", "' + self.name + '")')
				self.conn.commit()
				return True

	def get_reassembly_rule(self, line):
		try:
			temp = re.search(self.ar, line).group
		except AttributeError as e:
			temp = None
		if temp:
			if not self.already_exists('REASSEM_RULE', temp(1).lower()):
				try:
					rule_type = temp(2)
				except IndexError as e:
					rule_type = 'None'
				self.conn.execute('INSERT INTO REASSEM_RULE VALUES("' + temp(1) + '", "' + rule_type + '", "' + \
					self.current_d_rule + '", "' + self.name + '")')
				self.conn.commit()
				return True

	def get_substitution_rule(self, line):
		try:
			temp = re.search(self.sr, line).group
		except AttributeError as e:
			temp = None
		if temp:
			res = self.clean_group(temp)
			if not self.already_exists('SUBSTITUTION', res[0].lower()):
				try:
					self.conn.execute('INSERT INTO SUBSTITUTION VALUES("' + res[0].lower() + '", "' + \
						res[1].lower()	+ '", "' + self.name + '")')
					self.conn.commit()
					return True
				except IndexError as e:
					pass

	def get_equivalence_class(self, line):
		try:
			temp = re.search(self.er, line).group
		except AttributeError as e:
			temp = None
		if temp:
			if not self.already_exists('EQ', temp(1)):
				self.conn.execute('INSERT INTO EQ VALUES("' + temp(1) + '", "' + self.name + '")')
				self.conn.commit()
				return True

	def compile_re(self):
		self.st = re.compile(r'START: (.*)')
		self.kw = re.compile(r'Keyword: (.*)')
		self.dr = re.compile(r'D-Rule: (.*)')
		self.ar = re.compile(r'R-Rule: (.*)')
		self.sr = re.compile(r'Sub: (.*)')
		self.er = re.compile(r'Eq: (.*)')

	#Helper functions
	def clean_group(self, group):
		temp = re.sub('\(', '', group(1))
		temp = re.sub('\)', '', temp)
		temp = re.sub(' ', '', temp)
		res = re.split(',', temp)
		return res

	def already_exists(self, table, item):
		exists = False
		a = self.conn.execute('SELECT * FROM ' + table)
		for i in a:
			if item in i:
				exists = True
		return exists

class setup():

	def __init__(self):
		self.conn = sqlite3.connect('testdb')
		self.conn.execute('CREATE TABLE SCRIPT(__NAME TEXT)')
		self.conn.execute('CREATE TABLE OPENING(__NAME TEXT, __SCRIPT TEXT)')
		self.conn.execute('CREATE TABLE SUBSTITUTION(__NAME TEXT, SUBSTITUTION TEXT, __SCRIPT TEXT)')
		self.conn.execute('CREATE TABLE EQ(__NAME TEXT, __SCRIPT TEXT)')
		self.conn.execute('CREATE TABLE KEYWORD(__NAME TEXT, RANK INT, EQ TEXT, __SCRIPT TEXT)')
		self.conn.execute('CREATE TABLE DECOMP_RULE(__NAME TEXT, EQ TEXT, __SCRIPT TEXT)')
		self.conn.execute('CREATE TABLE REASSEM_RULE(__NAME TEXT, TYPE TEXT, D_RULE TEXT, __SCRIPT TEXT)')

if __name__ == '__main__':
	try:
		setup()
	except sqlite3.OperationalError as e:
		pass
	if len(sys.argv) > 1:
		ScriptReader(sys.argv[1])
	else:
		print('Please supply a script.')