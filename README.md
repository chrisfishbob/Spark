# Spark
Dynamically typed, eager evaluated programming language implemented in Python.  <br /><br /><br />

## Language Syntax Overview
The syntax of Spark can be captured as follows:
```
 Expr	=	Num
 	|	id
 	|	String
 	|	{if Expr Expr Expr}
 	|	{vars: [id = Expr] ... body: Expr}
 	|	{proc {id ...} go Expr}
 	|	{Expr Expr ...}
```

Spark currently supports 3 main types: integers, booleans, and strings. Values that get evaluated are printed directly to the terminal rather than a specific print function call.

For example, these lines:
```
(+ 1 2)
"Hello, World!"
1
```
prints "3", "Hello, World!", and "1" to the console respectively.



## Installation / Dependencies
The Spark interpreter requires Python@3.10 or above, to check your Python version:
```
python3 --version
```

The syntax of Spark uses the idea of s-expressions that's most commonly found in Lisp and since Python does not support s-expressions, Spark uses a s-expression parsing package that converts strings to lists.
```
pip3 install sexpdata
```
