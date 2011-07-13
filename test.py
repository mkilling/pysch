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

if __name__ == '__main__':
	unittest.main()