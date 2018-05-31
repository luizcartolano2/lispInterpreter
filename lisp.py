import re
import sys
import operator
import pprint as pretty_print

# defining utilities functions and data structures that will be usefull
pprint = lambda obj: pretty_print.PrettyPrinter(ident=4).pprint(obj)

def fail(s):
	print(s)
	sys.exit(-1)

class InterpreterObject(object):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return self.value

class Symbol(InterpreterObject):
	pass

class String(InterpreterObject):
	pass

class Lambda(InterpreterObject):
	def __init__(self, arguments, code):
		self.arguments = arguments
		self.code = code

	def __repr__(self):
		return "(lambda (%s) (%s)" % (self.arguments, self.code)

# making the parser function
def tokenize(s):
	ret = []
	in_string = False
	current_word = ''

	for i, char in enumerate(s):
		if in_string is False:	
			if char == "'":
				in_string = True
				current_word = current_word + char
			else:
				in_string = False
				current_word = current_word + char
				ret.append(current_word)
				current_word = ''
		elif in_string is True:
			current_word = current_word + char
		elif char in ['\t','\n',' ']:
			continue
		elif char in ['(',')']:
			ret.append(char)
		else:
			current_word = current_word + char
			if i < len(s) - 1 and s[i+1] in ['(',')',' ','\n','\t']:
				ret.append(current_word)
				current_word = ''

	return ret

# functions that will help convert tokens to their values
def is_integer(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
	
def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def is_string(s):
	try:
		if s[0] == "'" and s[-1] == "'"
			return True
	except ValueError:
		return False

# making the parser function now
def parse(tokens):
	itert = iter(tokens)
	token = itert.next()

	if token != '(':
		fail("Unexpected token {}".format(token))

	return do_parse(itert)

def do_parse(tokens):
	ret = []

	current_sexpr = None
	in_sexp = False

	for token in tokens:
		if token == '(':
			ret.append(do_parse(tokens))
		elif token == ')':
			return ret
		elif is_integer(token):
			ret.append(int(token))
		elif is_float(token):
			ret.append(float(token))
		elif is_string(token):
			ret.append(str(token[1:][0:-1]))
		else:
			ret.append(Symbol(token))



