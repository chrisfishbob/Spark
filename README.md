# Spark
Dynamically typed, eager evaluated programming language implemented in Python.  <br /><br/>


# REST API
Since I'm aware that you might not want to go through the hassle of installing Spark and its dependencies to try it out,
a public API is available to evaluate your Spark expressions in a POST call.

No API key is required for usage, but rate is capped at 2 requests per second per universe (more than anyone needs). Any API client will
work but here's a simple one in curl that you can just paste into your terminal if you have curl installed.

```
curl -X POST -d '{"expr": "(+ 1 2)"}' https://api.iamchrishsu.com/spark
```

<br /><br/>

# Installation / Dependencies
If you do want to give it a install:

The Spark interpreter requires Python@3.10 or above, to check your Python version:
```
python3 --version
```

The syntax of Spark uses the idea of s-expressions that's most commonly found in Lisp and since Python does not support s-expressions, Spark uses a s-expression parsing package that converts strings to lists.
```
pip3 install sexpdata
```

# Language Syntax Overview
The syntax of Spark can be captured as follows:
```
 Expr	=	Num
 	|	id
 	|	String
 	|	{if Expr Expr Expr}
 	|	{vars: [id = Expr] ... body: Expr}
 	|	{func {id ...} do Expr}
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
Evaluates to a lambda function that takes in x and y and applies the + operator. The function can be evaluated simply by passing in its parameters.

```
((func (x y) do (+ x y) 3 5)
```
Evaluates to 8


### Vars
Since Spark programs are written as a single expression, Spark has a built-in "vars" form to make coding easier:
```
(vars: (y = 3)
       (x = 5)
 body:
       (+ y x))
```

This is equivalent to the basic func form above and infact, parses to the same AST.



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
