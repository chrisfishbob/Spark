import unittest
from spark import *


class SparkTests(unittest.TestCase):
    def test_top_interp(self):
        self.assertEqual(top_interp('1'), 1)
        self.assertEqual(top_interp('23'), 23)
        self.assertEqual(top_interp('-70'), -70)
        self.assertEqual(top_interp('"Hello, world!"'), "Hello, world!")

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
        self.assertEqual(parse(SparkSymbol("+")), IdC("+"))
        self.assertEqual(parse(SparkSymbol("-")), IdC("-"))
        self.assertEqual(parse(SparkSymbol("*")), IdC("*"))
        self.assertEqual(parse(SparkSymbol("/")), IdC("/"))
        self.assertEqual(parse(SparkSymbol("true")), IdC("true"))
        self.assertEqual(parse(SparkSymbol("false")),
                         IdC("false"))

    def test_parse_ifc(self):
        self.assertEqual(parse(read("(if true 1 2)")), IfC(
            IdC("true"), NumC(1), NumC(2)))
        self.assertEqual(parse(read("(if true (+ 1 2) 2)")),
                         IfC(IdC("true"),
                             AppC(
                             IdC("+"), [NumC(1), NumC(2)]),
                             NumC(2)))

    def test_parse_lamc(self):
        self.assertEqual(parse(read("(proc (x y) go (+ 1 2))")),
                         LamC([SparkSymbol("x"), SparkSymbol("y")],
                              AppC(IdC("+"),
                                   [NumC(1), NumC(2)])))
        self.assertEqual(parse(read("(proc (x y) go (* x y))")),
                         LamC([SparkSymbol("x"), SparkSymbol("y")],
                              AppC(IdC("*"),
                                   [IdC("x"),
                                    IdC("y")])))


if __name__ == "__main__":
    unittest.main()
