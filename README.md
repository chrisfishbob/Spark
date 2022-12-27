# Spark
Dynamically typed, eager evaluated programming language implemented in Python.  <br /><br /><br />

# Language Syntax Overview
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

## Spark Example Programs
### Basic arithmetic operation:
```
(+ 1 2)
```
Outputs 3 <br />

### Nested evaluations
```
(+ (+ 1 2) 3)
```
Outputs 6 <br />

### Conditionals
```
(if (equals (+ 1 2)
            (+ 2 1))
    True
    False)
```
Outputs True, where as:<br />
```
(if (equals (- 1 2)
            (- 2 1))
    True
    False)
```
Outputs False.


### Functions
```
(func (x y) do (+ x y))
```
Evaluates to a lambda function that takes in x and y and applies the + operator.


### IO
Values that get evaluated are printed directly to the terminal rather than a specific print function call.

For example, these lines:
```
(+ 1 2)
"Hello, World!"
1
```
prints "3", "Hello, World!", and "1" to the console respectively.



# Installation / Dependencies
The Spark interpreter requires Python@3.10 or above, to check your Python version:
```
python3 --version
```

The syntax of Spark uses the idea of s-expressions that's most commonly found in Lisp and since Python does not support s-expressions, Spark uses a s-expression parsing package that converts strings to lists.
```
pip3 install sexpdata
```
