from typing import NamedTuple, Union
from sexpdata import loads, dumps, Symbol

class IfC(NamedTuple):
    test: "ExprC"
    then: "ExprC"
    otherwise: "ExprC"

class AppC(NamedTuple):
    func: "ExprC"
    args: list["ExprC"]


class IdC(NamedTuple):
    name: Symbol 

class NumC(NamedTuple):
    num: int 

class StrC(NamedTuple):
    string: str 

ExprC = Union[NumC, StrC, IdC, IfC, AppC] 


def main():
    s = loads('1')
    s1 = loads('(if true 1 2)')
    s2 = loads("(+ 1 2)")
    print(parse(s))
    print(parse(s1))
    print(parse(s2))


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
        case [Symbol(), test_cond, then, otherwise] if dumps(sexp[0]) == "if":
            return IfC(parse(test_cond), parse(then), parse(otherwise)) 
        case [func, *args]:
            return AppC(func, [parse(arg) for arg in args]) 
        case Symbol():
            return IdC(sexp)
        case _:
            return "Error while parsing"


if __name__ == "__main__":
    main()