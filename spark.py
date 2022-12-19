from typing import NamedTuple, Union
from sexpdata import loads, dumps, Symbol

class SparkSymbol(NamedTuple):
    symbol: str

class IfC(NamedTuple):
    test: "ExprC"
    then: "ExprC"
    otherwise: "ExprC"

class AppC(NamedTuple):
    func: "ExprC"
    args: list["ExprC"]

class IdC(NamedTuple):
    name: SparkSymbol

class NumC(NamedTuple):
    num: int 

class StrC(NamedTuple):
    string: str 


ExprC = Union[NumC, StrC, IdC, IfC, AppC] 


def main():
    s = loads('1')
    s1 = loads('(if true 1 2)')
    s2 = loads("(+ 1 2)")
    s3 = loads("(proc (x y) go (+ x 1))")
    print(replace_symbols(s1))
    print(parse(replace_symbols(s1)))


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
        case [SparkSymbol("if"), test_cond, then, otherwise]:
            return IfC(parse(test_cond), parse(then), parse(otherwise)) 
        case [SparkSymbol("proc"), [*params], Symbol(), body]:
            return "Proc"
        case [func, *args] if isinstance(sexp, list):
            return AppC(func, [parse(arg) for arg in args]) 
        case SparkSymbol(sy):
            return IdC(SparkSymbol(sy))
        case _:
            return "Error while parsing"


if __name__ == "__main__":
    main()