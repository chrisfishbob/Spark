import unittest
from spark import parse, IdC, IfC, NumC, StrC
from sexpdata import loads, Symbol

class SparkTests(unittest.TestCase):
    def test_parse_int(self):
        self.assertEqual(parse(1), NumC(1))
        self.assertEqual(parse(-1), NumC(-1))
        self.assertEqual(parse(0), NumC(0))
        self.assertEqual(parse(23), NumC(23))
        self.assertEqual(parse(100), NumC(100))
        self.assertEqual(parse(4000000), NumC(4000000))
        
    def test_parse_str(self):
        self.assertEqual(parse("testing"), StrC("testing"))
        self.assertEqual(parse(""), StrC(""))

    def test_parse_symbol(self):
        self.assertEqual(parse(Symbol("+")), IdC(Symbol("+")))
        self.assertEqual(parse(Symbol("-")), IdC(Symbol("-")))
        self.assertEqual(parse(Symbol("*")), IdC(Symbol("*")))
        self.assertEqual(parse(Symbol("/")), IdC(Symbol("/")))
        self.assertEqual(parse(Symbol("true")), IdC(Symbol("true")))
        self.assertEqual(parse(Symbol("false")), IdC(Symbol("false")))

    def test_parse_ifc(self):
        self.assertEqual(parse(loads("(if true 1 2)")), IfC(IdC(Symbol("true")), NumC(1), NumC(2)))


if __name__ == "__main__":
    unittest.main()