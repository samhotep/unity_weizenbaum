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
		#Load the welcome message for the specified script.
		self.script = script
		self.conn = sqlite3.connect('testdb')
		o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
		if len(o.fetchall()) > 0:
			o = self.conn.execute('SELECT * FROM OPENING WHERE __SCRIPT="' + self.script + '"')
			for opening in o:
				print('\n' + opening[0])
				while True:
					self.parse_input()
		else:
			print('The specified script does not exist. Did you check your spelling?')

	def parse_input(self):
		#Collect the user input for analysis.
		self.keystack = []
		self.sub_specials(input())
		self.substitute()
		self.transform()

	def sub_specials(self, user_input):
		user_input = re.sub(r'\?', '', user_input).lower()
		if ',' in user_input:
			user_input = user_input.split(',')[-1]
		self.user_inputs = user_input.strip().split(' ')

	def substitute(self):
		#Substitute selected words before rules are applied.
		counter, res = 0, []
		for i in self.user_inputs:
			subs = self.conn.execute('SELECT __NAME, SUBSTITUTION FROM SUBSTITUTION WHERE __NAME=="' + i + \
				'" AND __SCRIPT="' + self.script + '"')
			for j in subs:
				self.user_inputs[counter] = j[1]
			counter += 1
		#print(self.user_inputs) #Debug

	def transform(self):
		#Requires construction of regular expressions to look for decomposition rule matches.
		self.initialize_keystack()
		self.parse_decomposition_rules()

	def initialize_keystack(self):
		for i in self.user_inputs:
			#Scan input text for keywords, and sort them in a stack by rank
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
		#print(self.keystack) #Debug

	def parse_decomposition_rules(self):
		#Create a rule stack of decomposition rules from the equivalence class of the topmost keyword
		self.d_rule_stack = []
		try:
			decom = self.conn.execute('SELECT __NAME, EQ FROM DECOMP_RULE WHERE EQ=="' + self.keystack[0][0] + \
			'" AND __SCRIPT=="' + self.script + '"')
			for i in decom:
				self.d_rule_stack.append([i[0], i[1]])
				#print('Stack: ' + str(self.d_rule_stack)) #Debug
				#print(self.reconstruct_word(self.user_inputs)) #Debug	
			#Topmost decomposition rule determines how the word is reassembled
			self.assemble_reply(self.extract_response())
		except IndexError as e:
			print("I'm sorry, i don't understand")

	def extract_response(self):
		#Transform decomposition rule into a regex, and extract input components necessary for reassembly
		word = self.reconstruct_word(self.user_inputs)
		#print('word: ' + word) #Debug
		for i in self.d_rule_stack:
			res = self.clean_rule(i[0])
			#print('res: ' + str(res)) #Debug
			#print('res: ' + str(re.sub(r'\d', r'\s?(.*)\s?', str(res)))) #Debug
			regex = re.compile(re.sub(r'\d', r'\s?(.*)\s?', str(res)))
			#print(regex) #Debug
			match = re.search(regex, word)
			#print(match.groups()) #Debug
			responses = []
			if match:
				for j in match.groups():
					responses.append(j.strip())
				#print(responses) #Debug
				self.trans = i
				#print(self.trans[0]) #Debug
				return responses

	def assemble_reply(self, responses):
		#Use response values as well as stored reassembly rules to create a reply
		if responses:
			selected_rule, lowest_rank = '', 9999999999999999
			rules = self.conn.execute('SELECT * FROM REASSEM_RULE WHERE D_RULE=="' + self.trans[0] + \
				'" AND __SCRIPT=="' + self.script + '"')
			for i in rules:
				#Rules should be shuffled to prevent repetitiveness
				if int(i[3]) <= lowest_rank:
					lowest_rank = int(i[3])
					selected_rule = i[0]
				#print('R-RULE: ' + selected_rule)
			lowest_rank += 1
			self.conn.execute('UPDATE REASSEM_RULE SET RANK=' + str(lowest_rank) + ' WHERE __NAME=="' + \
				selected_rule + '"')
			self.conn.commit()
			for i in selected_rule:
				try:
					ref = int(i) - 1
				except ValueError as e:
					pass				
			cleaned_rule = self.clean_rule(selected_rule)
			#print('Clean: ' + cleaned_rule) #Debug
			#print(responses[ref]) #Debug
			try:
				self.reply = re.sub(r'\d', str(responses[ref]), cleaned_rule)
			except UnboundLocalError as e:
				self.reply = re.sub(r'\d', str(responses), cleaned_rule)
			print(self.reply.upper())

	#Helper functions
	def reconstruct_word(self, word):
		w = ''
		for i in word:
			w += i
			w += ' '
		w.strip()
		return w

	def clean_rule(self, rule):
		#print('Rule: ' + str(rule))
		rule = re.sub('\(', '', rule)
		rule = re.sub('\)', '', rule)
		rule = re.sub(r'\s?0\s?', '0', rule)
		return rule.strip()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		UNITY(sys.argv[1])
	else:
		print('Please specify a script.')