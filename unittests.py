import unittest
from spark import *


class SparkTests(unittest.TestCase):
    def test_top_interp(self):
        self.assertEqual(top_interp('1'), 1)
        self.assertEqual(top_interp('23'), 23)
        self.assertEqual(top_interp('-70'), -70)
        self.assertEqual(top_interp('"Hello, world!"'), "Hello, world!")
        self.assertEqual(top_interp('true'), True)
        self.assertEqual(top_interp('false'), False)
        self.assertEqual(top_interp("(+ 1 2)"), 3)
        self.assertEqual(top_interp("(- 1 2)"), -1)
        self.assertEqual(top_interp("(* 7 2)"), 14)
        self.assertEqual(top_interp("(/ 8 2)"), 4)
        self.assertEqual(top_interp("(equal 1 2)"), False)
        self.assertEqual(top_interp("(equal 2 2)"), True)
        self.assertEqual(top_interp("(equal (+ 1 2) (+ 2 1))"), True)

    def test_interp_int(self):
        self.assertEqual(interp(NumC(1), top_env), 1)
        self.assertEqual(interp(NumC(23), top_env), 23)

    def test_interp_string(self):
        self.assertEqual(interp(StrC("Hello"), top_env), "Hello")
        self.assertEqual(interp(StrC("World"), top_env), "World")

    def test_interp_if(self):
        self.assertEqual(
            interp(IfC(IdC("true"), NumC(1), NumC(2)), top_env), 1)
        self.assertEqual(
            interp(IfC(IdC("false"), NumC(1), NumC(2)), top_env), 2)
        self.assertEqual(
            interp(IfC(IdC("false"), NumC(1), NumC(2)), top_env), 2)
        self.assertEqual(
            interp(IfC(AppC(IdC("equal"), [NumC(7), NumC(7)]), NumC(1), NumC(2)), top_env), 1)
        self.assertEqual(
            interp(IfC(AppC(IdC("equal"), [NumC(8), NumC(7)]), NumC(1), NumC(2)), top_env), 2)
        self.assertEqual(
            interp(IfC(AppC(IdC("equal"), [NumC(8), NumC(7)]),
                       NumC(1),
                       AppC(IdC("*"), [NumC(5), NumC(6)])), top_env), 30)
        self.assertEqual(
            interp(IfC(AppC(IdC("equal"), [NumC(8), NumC(8)]),
                       AppC(IdC("*"), [NumC(5), NumC(7)]), 
                       AppC(IdC("*"), [NumC(5), NumC(6)])), top_env), 35)

    def test_interp_lamc(self):
        self.assertEqual(interp(LamC([SparkSymbol("x")], NumC(1)), top_env), CloV(
            [SparkSymbol("x")], NumC(1), top_env))
        self.assertEqual(interp(LamC([SparkSymbol("x"), SparkSymbol("y")], NumC(
            1)), top_env), CloV([SparkSymbol("x"), SparkSymbol("y")], NumC(1), top_env))

    def test_interp_id(self):
        self.assertEqual(interp(IdC("true"), top_env), True)
        self.assertEqual(interp(IdC("false"), top_env), False)
        self.assertEqual(interp(IdC("+"), top_env), PrimopV(SparkSymbol("+")))
        self.assertEqual(interp(IdC("-"), top_env), PrimopV(SparkSymbol("-")))
        self.assertEqual(interp(IdC("*"), top_env), PrimopV(SparkSymbol("*")))
        self.assertEqual(interp(IdC("/"), top_env), PrimopV(SparkSymbol("/")))

    def test_interp_appc(self):
        self.assertEqual(interp(AppC(LamC([SparkSymbol("x")], NumC(1)), [NumC(1)]), top_env), 1)
        self.assertEqual(interp(AppC(LamC([SparkSymbol("x"), SparkSymbol("y")], NumC(1)), [NumC(1), NumC(2)]), top_env), 1)
        self.assertEqual(interp(AppC(LamC([SparkSymbol("x"), SparkSymbol("y")], AppC(IdC("+"), [IdC("x"), IdC("y")])), [NumC(1), NumC(2)]), top_env), 3)
        with self.assertRaises(SyntaxError):
            interp(AppC(LamC([SparkSymbol("x"), SparkSymbol("y")], AppC(IdC("+"), [IdC("x"), IdC("y")])), [NumC(1)]), top_env)

    def test_interp_appc_primop(self):
        self.assertEqual(
            interp(AppC(IdC("+"), [NumC(1), NumC(2)]), top_env), 3)
        self.assertEqual(
            interp(AppC(IdC("-"), [NumC(1), NumC(2)]), top_env), -1)
        self.assertEqual(
            interp(AppC(IdC("*"), [NumC(5), NumC(2)]), top_env), 10)
        self.assertEqual(
            interp(AppC(IdC("/"), [NumC(16), NumC(4)]), top_env), 4)
        self.assertEqual(
            interp(AppC(IdC("equal"), [NumC(16), NumC(4)]), top_env), False)
        self.assertEqual(
            interp(AppC(IdC("equal"), [NumC(16), NumC(16)]), top_env), True)
        self.assertEqual(
            interp(AppC(IdC("equal"),
                        [NumC(16), AppC(IdC("+"), [NumC(4), NumC(12)])]), top_env), True)

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
        self.assertEqual(parse(read("(func (x y) do (+ 1 2))")),
                         LamC([SparkSymbol("x"), SparkSymbol("y")],
                              AppC(IdC("+"),
                                   [NumC(1), NumC(2)])))
        self.assertEqual(parse(read("(func (x y) do (* x y))")),
                         LamC([SparkSymbol("x"), SparkSymbol("y")],
                              AppC(IdC("*"),
                                   [IdC("x"),
                                    IdC("y")])))

    def test_primop_interp(self):
        self.assertEqual(primop_interp(PrimopV(SparkSymbol("+")), [1, 2]), 3)
        self.assertEqual(primop_interp(PrimopV(SparkSymbol("*")), [2, 2]), 4)
        self.assertEqual(primop_interp(PrimopV(SparkSymbol("/")), [4, 2]), 2)
        self.assertEqual(primop_interp(PrimopV(SparkSymbol("-")), [4, 2]), 2)
        self.assertEqual(primop_interp(
            PrimopV(SparkSymbol("<=")), [4, 2]), False)
        self.assertEqual(primop_interp(
            PrimopV(SparkSymbol("equal")), [4, 2]), False)
        self.assertEqual(primop_interp(
            PrimopV(SparkSymbol("equal")), [4, 4]), True)
        with self.assertRaises(TypeError):
            primop_interp(PrimopV(SparkSymbol("equal")), ["4", 4])

    def test_lookup(self):
        self.assertEqual(lookup(SparkSymbol("+"), top_env),
                         PrimopV(SparkSymbol("+")))
        self.assertEqual(lookup(SparkSymbol("-"), top_env),
                         PrimopV(SparkSymbol("-")))
        self.assertEqual(lookup(SparkSymbol("*"), top_env),
                         PrimopV(SparkSymbol("*")))
        self.assertEqual(lookup(SparkSymbol("/"), top_env),
                         PrimopV(SparkSymbol("/")))
        self.assertEqual(lookup(SparkSymbol("<="), top_env),
                         PrimopV(SparkSymbol("<=")))
        self.assertEqual(lookup(SparkSymbol("error"), top_env),
                         PrimopV(SparkSymbol("error")))
        self.assertEqual(lookup(SparkSymbol("equal"), top_env),
                         PrimopV(SparkSymbol("equal")))
        with self.assertRaises(Exception):
            lookup(SparkSymbol("invalid"), top_env)


if __name__ == "__main__":
    unittest.main()
