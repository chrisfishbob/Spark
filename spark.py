from typing import NamedTuple, Union
from sexpdata import loads, dumps, Symbol

ExprC = Union["NumC", "StrC", "IdC", "IfC", "AppC"]
Value = Union[int, bool, str, "CloV", "PrimopV"]


class SparkSymbol(NamedTuple):
    symbol_string: str


class Bind(NamedTuple):
    name: SparkSymbol
    value: Value


class Env(NamedTuple):
    bindings: list[Bind]


# Core expressions
class IdC():
    def __init__(self, symbol) -> None:
        self.symbol = SparkSymbol(symbol)

    def __repr__(self):
        return self.symbol.symbol_string

    def __eq__(self, other):
        return self.symbol == other


class IfC(NamedTuple):
    test: ExprC
    then: ExprC
    otherwise: ExprC


class AppC(NamedTuple):
    func: ExprC
    args: list[ExprC]


class NumC(NamedTuple):
    num: int


class StrC(NamedTuple):
    string: str


class LamC(NamedTuple):
    params: list[SparkSymbol]
    body: ExprC


# Values
class CloV(NamedTuple):
    params: list[SparkSymbol]
    body: ExprC
    env: Env


class PrimopV(NamedTuple):
    op: SparkSymbol


# Top Level Environment
top_env = Env([Bind(SparkSymbol("true"), True),
              Bind(SparkSymbol("false"), False),
              Bind(SparkSymbol("+"), PrimopV(SparkSymbol("+"))),
              Bind(SparkSymbol("-"), PrimopV(SparkSymbol("-"))),
              Bind(SparkSymbol("*"), PrimopV(SparkSymbol("*"))),
              Bind(SparkSymbol("/"), PrimopV(SparkSymbol("/"))),
              Bind(SparkSymbol("<="), PrimopV(SparkSymbol("<="))),
              Bind(SparkSymbol("error"), PrimopV(SparkSymbol("error"))),
              Bind(SparkSymbol("equal?"), PrimopV(SparkSymbol("equal?")))])


def main():
    s1 = '(if true 1 2)'
    s2 = "(+ 1 2)"
    s3 = "(proc (x y) go (+ x 1))"


def replace_symbols(sexp):
    if isinstance(sexp, Symbol):
        return SparkSymbol(dumps(sexp))

    if isinstance(sexp, list):
        for index, e in enumerate(sexp):
            if isinstance(e, Symbol):
                sexp[index] = SparkSymbol(dumps(e))
            if isinstance(e, list):
                replace_symbols(e)

    return sexp


def read(program: str):
    return replace_symbols(loads(program))


def interp(expr: ExprC):
    match expr:
        case NumC(n):
            return n
        case StrC(s):
            return s


def parse(sexp):
    match sexp:
        case int():
            return NumC(sexp)
        case str():
            return StrC(sexp)
        # (if test then otherwise)
        case [SparkSymbol("if"), test_cond, then, otherwise]:
            return IfC(parse(test_cond), parse(then), parse(otherwise))
        # (proc (args) go body)
        case [SparkSymbol("proc"), [*params], SparkSymbol("go"), body]:
            return LamC(params, parse(body))
        # (+ 1 2)
        case [func, *args] if isinstance(sexp, list):
            return AppC(parse(func), [parse(arg) for arg in args])
        # `true
        case SparkSymbol(sy):
            return IdC(sy)
        case _:
            return "Error while parsing"


if __name__ == "__main__":
    main()
