from typing import NamedTuple, Union
from sexpdata import loads, dumps, Symbol
import sys

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

class RecC(NamedTuple):
    name: SparkSymbol
    params: list[SparkSymbol]
    recursive_body: ExprC
    program_body: ExprC
    


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
              Bind(SparkSymbol("equal"), PrimopV(SparkSymbol("equal")))])


def main():
    # If there is no additional arguments, just print "hello"
    if len(sys.argv) == 1:
        while True:
            program = input("spark> ")
            top_interp(program)
    else:
        with open(sys.argv[1]) as f:
            program = f.read()
            top_interp(program)


# Given the user program, return the interpreted value
def top_interp(program: str):
    print(interp(parse(read(program)), top_env))


# Given the user program as a string, return the program in s-expression form
def read(program: str):
    return replace_symbols(loads(program))


# Given an ExprC expression, evaluate its output
def interp(expr: ExprC, env: Env) -> Value:
    match expr:
        case NumC(n):
            return n
        case StrC(s):
            return s
        case IfC(condition, then, otherwise):
            condition_result = interp(condition, env)
            if condition_result:
                return interp(then, env)
            else:
                return interp(otherwise, env)
        case LamC(params, body):
            return CloV(params, body, env)
        case IdC(symbol=s):
            return lookup(s, env)

        case AppC(func, args):
            func_value = interp(func, env)
            if isinstance(func_value, CloV):
                if len(args) != len(func_value.params):
                    raise SyntaxError(
                        f"Expected {len(func_value.params)} arguments, got {len(args)}")

                arg_vals = [interp(arg, env) for arg in args]
                new_env = Env(func_value.env.bindings +
                              [Bind(param, arg) for param, arg in zip(func_value.params, arg_vals)])
                return interp(func_value.body, new_env)

            elif isinstance(func_value, PrimopV):
                return primop_interp(func_value, [interp(arg, env) for arg in args])
            else:
                raise SyntaxError(f"Cannot apply non-function {func_value}")


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
        case [SparkSymbol("func"), [*params], SparkSymbol("do"), body]:
            return LamC(params, parse(body))
        # vars
        case [SparkSymbol("vars:"), *vars, SparkSymbol("body:"), body]:
            var_symbols = {v[0] for v in vars}
            var_arguments = [parse(v[2]) for v in vars]
            return AppC(LamC(var_symbols, parse(body)), var_arguments)
        # (+ 1 2)
        case [func, *args] if isinstance(sexp, list):
            return AppC(parse(func), [parse(arg) for arg in args])
        # `true
        case SparkSymbol(sy):
            return IdC(sy)
        case _:
            return "Error while parsing"


def primop_interp(op: PrimopV, args: list[Value]) -> Value:
    match op, args:
        case PrimopV(SparkSymbol("+")), [n1, n2]:
            return n1 + n2
        case PrimopV(SparkSymbol("-")), [n1, n2]:
            return n1 - n2
        case PrimopV(SparkSymbol("*")), [n1, n2]:
            return n1 * n2
        case PrimopV(SparkSymbol("/")), [n1, n2]:
            return n1 / n2
        case PrimopV(SparkSymbol("<=")), [n1, n2]:
            return n1 <= n2
        case PrimopV(SparkSymbol("equal")), [v1, v2]:
            if type(v1) == type(v2):
                return v1 == v2
            raise TypeError(f"Types much match for equal? comparision")

        case PrimopV(SparkSymbol("error")), [error_message]:
            raise RuntimeError(f"User error: {error_message}")
        case _:
            raise RuntimeError(
                "Spark Error: Failed to match in primop iinterp")


def lookup(target: SparkSymbol, env: Env) -> Value:
    for bind in env.bindings:
        if bind.name == target:
            return bind.value

    raise LookupError(f"Symbol not found in environment: {env}")


# Given a parsed s-expression, replace all instaces of Symbol with SparkSymbol
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


if __name__ == "__main__":
    main()
