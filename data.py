import sqlite3, re, sys

class Keyword():
	"""Determines how input text is sorted and transformed"""
	def __init__(self, rank):
		self.rank = rank

'''We start by selecting a script from the db. Having done this, the opening phrase is loaded as pertaining to this
script, then printed to the user. The next task is to parse user input, according to rules stored in the database.i.e
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
		if len(o.fetchall()) > 0:
			o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
			for opening in o:
				opening[1]
				print('\n' + opening[0])
				self.parse_input()
		else:
			print('The specified script does not exist. Did you check your spelling?')

	def parse_input(self):
		user_input = input()
		self.keystack = []
		self.user_inputs = user_input.strip().split(' ')
		self.substitute()
		self.decompose()

	def substitute(self):
			counter, res = 0, []
			for i in self.user_inputs:
				subs = self.conn.execute('SELECT __NAME, SUBSTITUTION FROM SUBSTITUTION WHERE __NAME=="' + i + \
					'" AND __SCRIPT="' + self.script + '"')
				for j in subs:
					self.user_inputs[counter] = j[1]
				counter += 1
			print(self.user_inputs) #Debug

	def decompose(self):
		#Requires construction of regular expressions to look for decomposition rule matches.
		self.initialize_keystack()
		self.parse_decomposition_rules()

	def initialize_keystack(self):
		for i in self.user_inputs:
			keys = self.conn.execute('SELECT RANK, EQ FROM KEYWORD WHERE __NAME=="' + i + \
				'" AND __SCRIPT=="' + self.script + '"')
			if len(keys.fetchall()) != 0:
				keys = self.conn.execute('SELECT RANK, EQ FROM KEYWORD WHERE __NAME=="' + i + \
				'" AND __SCRIPT=="' + self.script + '"')
				for j in keys:
					rank, eq = j[0], j[1]
				add = False
				if len(self.keystack) == 0:
					self.keystack.append([i, rank])
				else:
					for y in self.keystack:
						if not i in y:
							add = True
				if add:
					self.keystack.append([i, rank])
				self.keystack.sort(key= lambda s: s[1], reverse=True)
		print(self.keystack) #Debug

	def parse_decomposition_rules(self):
		self.d_rule_stack = []
		try:
			decom = self.conn.execute('SELECT __NAME, EQ FROM DECOMP_RULE WHERE EQ=="' + self.keystack[0][0] + \
			'" AND __SCRIPT=="' + self.script + '"')
			for i in decom:
				self.d_rule_stack.append([i[0], i[1], 0])
				print(self.d_rule_stack) #Debug
				print(self.reconstruct_word(self.user_inputs)) #Debug	
			self.extract_response()
		except IndexError as e:
			print("I'm sorry, i don't understand")

	def extract_response(self):
		#Transform decomposition rule into a regex, and extract the components necessary for reassembly
		word = self.reconstruct_word(self.user_inputs)
		print('word: ' + word) #Debug
		for i in self.d_rule_stack:
			res = self.clean_rule(i[0])
			print('res: ' + str(res)) #Debug
			regex = re.compile(re.sub(r'\d', r'(.*)', str(res)))
			print(regex) #Debug
			match = re.search(regex, word)
			responses = []
			if match:
				for i in match.groups():
					responses.append(i.strip())
			print(responses)

	#Helper functions
	def reconstruct_word(self, word):
		w = ''
		for i in word:
			w += i
			w += ' '
		w.strip()
		return w

	def clean_rule(self, rule):
		print('Rule: ' + str(rule))
		rule = re.sub('\(', '', rule)
		rule = re.sub('\)', '', rule)
		return rule	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		UNITY(sys.argv[1])
	else:
		print('Please specify a script.')