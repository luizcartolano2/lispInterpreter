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
		if s[0] == "'" and s[-1] == "'":
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

# making the interpreter
def eval(expr, environment):
	if isinstance(expr, int):
	    return expr
	elif isinstance(expr, str):
	    return expr
	elif isinstance(expr, float):
	    return expr
	elif isinstance(expr, String):
	    return expr.value
	elif isinstance(expr, Symbol):
	    if expr.value not in environment:
	        fail("Couldn't find symbol {}".format(expr.value))
	    return environment[expr.value]
	elif isinstance(expr, list):
		if isinstance(expr[0], Symbol):
			if expr[0].value == 'lambda':
				arg_names = expr[1]
				code = expr[2]
				return Lambda(arg_names, code)
	elif expr[0].value == 'if':
		condition = expr[1]
		then = expr[2]
		_else = None
		if len(expr) == 4:
		    _else = expr[3]

		if eval(condition, environment) != False:
		    return eval(then, environment)
		elif _else is not None:
		    return eval(_else, environment)
	elif expr[0].value == 'define':
		name = expr[1].value
		value = eval(expr[2],environment)
		environment[name] = value
	elif expr[0].value == 'begin':
		for ex in expr[1:]:
			eval(ex,environment)
	else:
		fn = eval(expr[0],environment)
		args = [eval(arg,environment) for arg in expr[1:]]
		return apply(fn, args, environment)

def apply(fn, args, environment):
	if callable(fn):
		return fn*args

	if isinstance(fn, Lambda):
		new_env = dict(environment)
		if len(args) != len(fn.arguments):
			fail("Mismatched number of arguments to lambda")
		for i in range(len(fn.arguments)):
			new_env[fn.arguments[i].value] = args[i]


		return eval(fn.code, new_env)

base_environment = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '!=': operator.ne,
    'nil': None,
    'print': lambda x: sys.stdout.write(str(x) + '\n'),
}

# defining main function
def main():
	if len(sys.argv) != 2:
		print "usage: python {} <file>".format(sys.argv[0])
		exit(-1)

	with open(sys.argv[1]) as fd:
		contents = fd.read()
		parsed = parse(tokenize(contents))
		eval(parsed, base_environment)

if __name__ == '__main__':
	main()




