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
		self.conn = sqlite3.connect('testdb')
		o = self.conn.execute('SELECT * FROM OPENING WHERE SCRIPT="' + self.script + '"')
		for opening in o:
			try:
				opening[1]
				print(opening[0])
				self.parse_input(input())
			except IndexError as e:
				pass

	def parse_input(self, user_input):
		self.user_input = user_input
		self.substitute()

	def substitute(self):
		subs = self.conn.execute('SELECT NAME, SUBSTITUTION FROM SUBSTITUTION WHERE SCRIPT="' + self.script + '"')
		for i in subs:
			if i[0] in self.user_input:
				self.subbed_input = re.sub(i[0], i[1], self.user_input)
				print(self.subbed_input)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		UNITY(sys.argv[1])