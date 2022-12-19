from typing import NamedTuple
from sexpdata import loads, dumps, Symbol

class IfC(NamedTuple):
    test: any
    then: any
    otherwise: any

class IdC(NamedTuple):
    name: Symbol 

class NumC(NamedTuple):
    num: int 

class StrC(NamedTuple):
    string: str 


    
def main():
    s = loads('1')
    s1 = loads('(if true 1 2)')
    # print(s1)
    # print(type(s1[0]))
    print(parse(s1))
    print(parse("+"))

def parse(sexp):
    match sexp:
        case int():
            return NumC(sexp)
        case str():
            return StrC(sexp)
        case [Symbol(), test_cond, then, otherwise] if dumps(sexp[0]) == "if":
            return IfC(parse(test_cond), parse(then), parse(otherwise)) 
        case Symbol():
            return IdC(sexp)
        case _:
            return "Error while parsing"


if __name__ == "__main__":
    main()