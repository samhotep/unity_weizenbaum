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
		o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
		for opening in o:
			try:
				opening[1]
				print(opening[0])
				self.parse_input(input())
			except IndexError as e:
				pass

	def parse_input(self, user_input):
		self.user_inputs = user_input.strip().split(' ')
		self.substitute()

	def substitute(self):
		counter, res = 0, []
		for i in self.user_inputs:
			subs = self.conn.execute('SELECT __NAME, SUBSTITUTION FROM SUBSTITUTION WHERE __NAME==	"' + i + 
				'" AND __SCRIPT="' + self.script + '"')
			for j in subs:
				print(i + ':')
				print(j)
				self.user_inputs[counter] = j[1]
			counter += 1
		print(self.user_inputs)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		UNITY(sys.argv[1])
	else:
		print('Please specify a script.')