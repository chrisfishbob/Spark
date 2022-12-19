from sexpdata import loads, dumps

def main():
    s = loads('1')
    print(parse(s))

def parse(sexp):
    match sexp:
        case int() | float() | str():
            return sexp
        case _:
            print("Error while parsing")


if __name__ == "__main__":
    main()