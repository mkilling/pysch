def exp_as_list(exp):
	ret = []
	def get_first(exp):
		exp = exp.strip()
		if exp.startswith('('):
			ct = 1
			idx = 1
			while ct > 0:
				if exp[idx] == '(':
					ct += 1
				elif exp[idx] == ')':
					ct -= 1
				idx += 1
			return exp[:idx], exp[idx:]
		else:
			first_space = exp.find(' ')
			if first_space > 0:
				return exp[:first_space], exp[first_space+1:]
			else:
				return exp, ""
	if exp.startswith('(') and exp.endswith(')'):
		exp = exp[1:-1]
	while len(exp) > 0:
		first, exp = get_first(exp)
		ret.append(first)
	return ret

class Proc:
	def __init__(self, env):
		self.env = env
	def apply(self, args):
		raise NotImplemented()

class CompoundProcedure(Proc):
	def __init__(self, exp, env):
		Proc.__init__(self, env)
		lst = exp_as_list(exp)
		self.params = exp_as_list(lst[1])
		self.body = lst[2:]
	def apply(self, args):
		new_env = extend_environment(dict(zip(self.params, args)), self.env)
		stmts = eval_sequence(self.body, new_env)
		return stmts[-1]

class PlusProc(Proc):
	def __init__(self, env):
		Proc.__init__(self, env)
	def apply(self, args):
		return str(sum(map(float, map(lambda x: eval(x, self.env), args))))
		
class MinusProc(Proc):
	def __init__(self, env):
		Proc.__init__(self, env)
	def apply(self, args):
		acc = float(eval(args[0], self.env))
		acc -= sum(map(float, map(lambda x: eval(x, self.env), args[1:])))
		return str(acc)

class MultProc(Proc):
	def __init__(self, env):
		Proc.__init__(self, env)
	def apply(self, args):
		acc = 1
		for exp in args:
			acc *= float(eval(exp, self.env))
		return str(acc)

def lookup_var(name, env):
	for frame in env:
		if name in frame:
			return frame[name]
	raise Exception("var not found: " + name)

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
	raise Exception("var not found: " + name)


def quoted_value(exp):
	if exp.startswith("'"):
		return exp[1:]
	else:
		raise Exception("not implemented")
		
def eval_assignment(exp, env):
	parts = exp.strip('()').split(' ')
	set_var(parts[1], parts[2], env)
	
def eval_definition(exp, env):
	parts = exp.strip('()').split(' ')
	define_var(parts[1], parts[2], env)

def eval_if(exp, env):
	lst = exp_as_list(exp)
	if is_true(lst[1], env):
		return eval(lst[2], env)
	else:
		return eval(lst[3], env)

def eval_sequence(exps, env):
	return map(lambda exp: eval(exp, env), exps)

def is_true(exp, env):
	return eval(exp, env) != '#f'

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def is_string(s):
	import re
	return re.match("\\\"[^\\\"]*\\\"$", s) != None

def is_bool(s):
	return s == '#f'

def is_self_evaluating(exp):
	return is_string(exp) or is_number(exp) or is_bool(exp)

def is_variable(exp):
	return not (exp.startswith("(") or " " in exp)
	
def is_quoted(exp):
	return exp.startswith("(quote") or exp.startswith("'")
	
def is_definition(exp):
	return exp.startswith("(define")

def is_assignment(exp):
	return exp.startswith("(set!")

def is_lambda(exp):
	return exp.startswith("(lambda")

def is_application(exp):
	return len(exp_as_list(exp)) > 1

def is_if(exp):
	return exp.startswith("(if")

def is_cond(exp):
	return exp.startswith("(cond")
	
def is_begin(exp):
	return exp.startswith("(begin")

def eval(exp, env):
	if is_self_evaluating(exp):
		return exp
	elif is_variable(exp):
		return lookup_var(exp, env)
	elif is_quoted(exp):
		return quoted_value(exp)
	elif is_assignment(exp):
		return eval_assignment(exp, env)
	elif is_definition(exp):
		return eval_definition(exp, env)
	elif is_if(exp):
		return eval_if(exp, env)
	elif is_lambda(exp):
		return CompoundProcedure(exp, env)
	elif is_begin(exp):
		return eval_sequence(exp_as_list(exp)[1:], env)
	elif is_cond(exp):
		pass
	elif is_application(exp):
		lst = exp_as_list(exp)
		if lst[0] == '+':
			proc = PlusProc(env)
		elif lst[0] == '-':
			proc = MinusProc(env)
		elif lst[0] == '*':
			proc = MultProc(env)
		else:
			proc = eval(lst[0], env)
		return proc.apply(lst[1:])
	else:
		raise Exception("unknown expression type " + exp)
