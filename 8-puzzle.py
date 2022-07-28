# Imports

from os import system
from random import choice

# Globals

it_lim = 1000000
random_table = 1

# Classes

class Node():

	__slots__ = ['matrix', 'i', 'j', 'g', 'f']

	def __init__(self, matrix, i, j, g):
		self.matrix = matrix
		self.g = g
		self.i = i
		self.j = j
		self.f = None
		pass

	# Util

	def copy(self):
		draft = []
		for i in self.matrix:
			line = []
			for j in i:
				line.append(j)
			draft.append(line)
		return Node(draft, self.i, self.j, self.g)

	def moveup(self):
		if self.i > 0:
			self.matrix[self.i][self.j] = self.matrix[self.i - 1][self.j]
			self.matrix[self.i - 1][self.j] = 0
			self.i -= 1
		return self

	def movedown(self):
		if self.i < 2:
			self.matrix[self.i][self.j] = self.matrix[self.i + 1][self.j]
			self.matrix[self.i + 1][self.j] = 0
			self.i += 1
		return self

	def moveleft(self):
		if self.j > 0:
			self.matrix[self.i][self.j] = self.matrix[self.i][self.j - 1]
			self.matrix[self.i][self.j - 1] = 0
			self.j -= 1
		return self

	def moveright(self):
		if self.j < 2:
			self.matrix[self.i][self.j] = self.matrix[self.i][self.j + 1]
			self.matrix[self.i][self.j + 1] = 0
			self.j += 1
		return self

	def toString(self):
		text = '\n\t'
		for line in self.matrix:
			for item in line:
				if item: text += str(item) + ' '
				else: text += '- '
			text += '\n\t'
		return text

class Puzzle(): # 8-puzzle.

	__slots__ = ['initial', 'it_lim']

	def __init__(self):
		self.it_lim = 100000
		self.initial = None

	def findemptyslot(self, matrix):
		for i in range(3):
			for j in range(3):
				if not matrix[i][j]:
					return (i, j)
		return None

	def accept(self, matrix):
		emptyslot = self.findemptyslot(matrix)
		self.initial = Node(matrix, i=emptyslot[0], j=emptyslot[1], g=0)
		return

	def random(self):
		
		self.initial = Node([
			[0, 1, 2],
			[3, 4, 5],
			[6, 7, 8]],
			i=0, j=0, g=0)

		for i in range(250):
			move = choice([1,2,3,4])
			if   move == 1: self.initial.moveup()
			elif move == 2: self.initial.moveleft()
			elif move == 3: self.initial.moveright()
			elif move == 4: self.initial.movedown()

		return None		
	
	def solve(self): # solve the puzzle.
		if self.initial:
			self.initial.f = self.function(self.initial)
			return self.RBFS(self.initial, f_limit=2**31-1)
		else: print('\n\tThere is no puzzle to solve.')

	def h(self, node):
		h = 0
		for l in range(3):
			for c in range(3):
				tag = node.matrix[l][c]
				if tag:
					h += abs(l - tag // 3) + abs(c - tag % 3)
		return h

	def function(self, node):
		return self.h(node) + node.g

	def generatesuccessors(self, node):
		successors = []

		if node.i > 0:
			clone = node.copy().moveup()
			clone.g += 1
			clone.f = self.function(clone)
			successors.append(clone)
		if node.i < 2:
			clone = node.copy().movedown()
			clone.g += 1
			clone.f = self.function(clone)
			successors.append(clone)
		if node.j > 0:
			clone = node.copy().moveleft()
			clone.g += 1
			clone.f = self.function(clone)
			successors.append(clone)
		if node.j < 2:
			clone = node.copy().moveright()
			clone.g += 1
			clone.f = self.function(clone)
			successors.append(clone)

		return successors

	def selectnodes(self, nodes):
		best = nodes[0]
		alternative = nodes[1]
		for node in nodes[1:]:
			if node.f < best.f:
				alternative = best
				best = node
			elif node.f < alternative.f:
				alternative = node
		return best, alternative

	def RBFS(self, node:Node, f_limit:int): # Recursive Best-First Search
		
		if self.checkgoal(node): return ([node], node.f)

		successors = self.generatesuccessors(node)

		while self.it_lim:

			selected = self.selectnodes(successors)

			self.it_lim -= 1

			if selected[0].f > f_limit:
				return ([], selected[0].f)

			aux = self.RBFS(selected[0], min(f_limit, selected[1].f))
			
			if aux[0]: # a path was found,
				aux[0].insert(0, node) # add the current node to it
				return aux # return the refined path.
			else:
				selected[0].f = aux[1] # failure, update the heuristic and try again.
		return ([], 0)

	def checkgoal(self, node): # check whether we're at the final node.
		for i in range(3):
			for j in range(3):
				if node.matrix[i][j] != 3*i + j: return False
		return True

# Functions

def banner():
	global it_lim, random_table
	print('\n\tSettings\n' +
		  '\n\tIteration Limit: ' + str(it_lim) + '.\n' + 
		    '\tRandom Matrix: ' + str(bool(random_table)) + '.\n' +
		     '_' * 100)
	return

def helpbanner():
	print('\n\t+In the 8-puzzle, the player needs to move the tiles in order to sort the board.\n'
		'\tThis program uses a recursive AI algorithm named A* Search with memory bounds to find a sequence\n'
		"\tof moves that set the table to it's original form.\n\n"
		"\t+ Set an iteration limit to bound the algorithm's range.\n"
		"\t+ Choose between entering a board or letting the program generate a random one.\n"
		"\t  A random board is sure to be solved whereas a user board may not.\n"
		"\t+ Type '0' where the empty tile goes."
		)
	input('\n\tENTER to continue.')
	return

def menu():
	op = input('\n\tSelect\n\n'
			'\t(B) to start.\n'
			'\t(S) to change settings.\n'
			'\t(H) to see help.\n'
			'\t(ANY) to quit.\n\n\t').lower()
	return op

def read():
	print('\n\tType each line of the board:\n')
	matrix = []
	for i in range(3):
		matrix.append(list(map(int, input('\t').split())))
	return matrix

def initialize():

	global it_lim, random_table

	puzzle = Puzzle()
	puzzle.it_lim = it_lim

	if random_table: puzzle.random()
	else: puzzle.accept(read())

	system('cls')
	print('\n\tInitial State')
	print(puzzle.initial.toString())

	path = puzzle.solve()
	if path[1]:
		print(f'''\t{it_lim - puzzle.it_lim} iterations needed.\n\n\tResolution Path - {len(path[0])} steps.''')
		for node in path[0]: print(node.toString())
	else:
		print(f'''\tNo solution was found after {it_lim - puzzle.it_lim} iterations.\n''')

	input('\n\tENTER to continue.')
	return

def configure():
	global it_lim, random_table
	it_lim = int(input('\n\tInsert an iteration limit: '))
	random_table = int(input('\n\t(0) to user mode.' +
							 '\n\t(ANY) to random mode.\n\t'))
	return

# Main

while True:

	banner()
	user_op = menu()

	if user_op == 'b':
		system('cls')
		initialize()
	elif user_op == 's':
		system('cls')
		configure()
	elif user_op == 'h':
		system('cls')
		helpbanner()
	else:
		break

	system('cls')