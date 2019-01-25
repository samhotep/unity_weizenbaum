from data import *
import sqlite3

class main():
	def __init__(self):
		self.list_scripts()
		self.get_user_input()

	def list_scripts(self):
		print('These are the available scripts. More to be added soon.')
		self.conn = sqlite3.connect('testdb')
		scripts = self.conn.execute('SELECT * FROM SCRIPT')
		counter = 1
		for i in scripts:
			print(str(counter) + ': ' + i[0])
			counter += 1

	def get_user_input(self):
		print('\nPlease type in the name of the script to be used.')
		user_input = input()
		UNITY(user_input)

if __name__ == '__main__':
	main()