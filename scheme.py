def lookup_var(name, env):
	for frame in env:
		if name in frame:
			return frame[name]
	raise "var not found: " + name

def define_var(name, val, env):
	if not name in env[0]:
		env[0][name] = val

def extend_environment(frame, env):
	return [frame] + env
	
def set_var(name, val, env):
	for frame in env:
		if name in frame:
			frame[name] = val
			return
	raise "var not found: " + name


def quoted_value(exp):
	if exp.startswith("'"):
		return exp[1:]
	else:
		raise "not implemented"
		
def eval_assignment(exp, env):
	parts = exp.strip('()').split(' ')
	set_var(parts[1], parts[2], env)
	
def eval_definition(exp, env):
	parts = exp.strip('()').split(' ')
	define_var(parts[1], parts[2], env)

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def is_string(s):
	import re
	return re.match("\\\"[^\\\"]*\\\"$", s) != None

def self_evaluating(exp):
	return is_string(exp) or is_number(exp)

def variable(exp):
	return not (exp.startswith("(") or " " in exp)
	
def quoted(exp):
	return exp.startswith("(quote") or exp.startswith("'")
	
def definition(exp):
	return exp.startswith("(define")

def assignment(exp):
	return exp.startswith("(set!")

def eval(exp, env):
	if self_evaluating(exp):
		return exp
	elif variable(exp):
		return lookup_var(exp, env)
	elif quoted(exp):
		return quoted_value(exp)
	elif assignment(exp):
		return eval_assignment(exp, env)
	elif definition(exp):
		 return eval_definition(exp, env)
	else:
		raise "unknown expression type " + exp