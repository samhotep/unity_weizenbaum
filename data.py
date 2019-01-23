import sqlite3, re, sys

class Keyword():
	"""Determines how input text is sorted and transformed"""
	def __init__(self, rank):
		self.rank = rank

'''We start by selecting a script from the db. Having done this, the opening phrase is loaded as pertaining to this
script, then printed to the user. The next task is to parse user input, according to rules stored in the database. i.e
1. Substitution
2. Decomposition
3. Transformation
4. Reassembly.
'''
class UNITY():

	def __init__(self, script):
		self.script = script
		self.keystack = []
		self.conn = sqlite3.connect('testdb')
		o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
		if len(o.fetchall()) > 0:
			o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
			for opening in o:
				opening[1]
				print(opening[0])
				self.parse_input(input())
		else:
			print('The specified script does not exist. Did you check your spelling?')

	def parse_input(self, user_input):
		self.user_inputs = user_input.strip().split(' ')
		self.substitute()
		self.decompose()

	def substitute(self):
		counter, res = 0, []
		for i in self.user_inputs:
			subs = self.conn.execute('SELECT __NAME, SUBSTITUTION FROM SUBSTITUTION WHERE __NAME=="' + i + \
				'" AND __SCRIPT="' + self.script + '"')
			for j in subs:
				print(i + ':')
				print(j)
				self.user_inputs[counter] = j[1]
			counter += 1
		print(self.user_inputs)

	def decompose(self):
		for i in self.user_inputs:
			keys = self.conn.execute('SELECT RANK, EQ FROM KEYWORD WHERE __NAME=="' + i + \
				'" AND __SCRIPT=="' + self.script + '"')
			for j in keys:
				rank, eq = j[0], j[1]
			add = False
			for y in self.keystack:
				if not i in y:
					add = True
			if add:
				self.keystack.append([i, rank])
			self.keystack.sort(key= lambda s: s[1])
		print(self.keystack)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		UNITY(sys.argv[1])
	else:
		print('Please specify a script.')