import scheme
import unittest

class TestScheme(unittest.TestCase):
	def test_arithmetic(self):
		self.assertEqual(scheme.eval("(+ 1 (* 1 2) (- 5 2))", [{}]), '6.0')
	
	def test_define(self):
		define_env = [{}]
		scheme.eval("(define a 5.0)", define_env)
		self.assertEqual(scheme.eval("a", define_env), '5.0')
	
	def test_lambda(self):
		self.assertEqual(scheme.eval("((lambda (a b) (+ a b)) 5 7)", [{}]), '12.0')
	
	def test_procedural_lambda(self):
		self.assertEqual(scheme.eval("((lambda (a b) (+ 1 1) (+ a b)) 5 7)", [{}]), '12.0')
	
	def test_assignment(self):
		env = [{}]
		scheme.eval("(define a 10.0)", env)
		self.assertEqual(scheme.eval("a", env), '10.0')
		scheme.eval("(set! a 12.0)", env)
		self.assertEqual(scheme.eval("a", env), '12.0')
		
	def test_if(self):
		self.assertEqual(scheme.eval("(if #f 1.0 10.0)", [{}]), '10.0')
		self.assertEqual(scheme.eval("(if 10 1.0 10.0)", [{}]), '1.0')
	
	def test_strings(self):
		self.assertEqual(scheme.eval('(if #f "true" "false")', [{}]), '"false"')

if __name__ == '__main__':
	unittest.main()