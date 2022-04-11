<div align="center">
    <br>
    <img alt="Mini-Lang logo" src="assets/logo_small.png" width="350px"/>
    <p>
    <br>
        <b>The mini programming language</b> built for the<br>
        <a href="https://dev.to/williamragstad/series/17603" about="_blank">
            <em>Write a language in a week</em>
        </a> series.
    </p>
    <br>
</div>

# The `mini` language

This is the repository for the example programming language `mini` built for the [*Write a language in a week*](https://dev.to/williamragstad/series/17603) series. Read the full series.

`mini` is a minmal programming language that is built for the purpose of teaching programming language design.
The language is dynamically typed expression-based, and is designed to be easy to learn and use. There are support for both functional and object oriented programming paradigms.

It is not intended to be a full language, but rather a language that can be expanded upon and explore new and more advanced concepts in language design.


## Features

The language has a rich set of features, including:

* Basic arithmetic, logic, and comparison operators
* Primitive data types such as `number`, `boolean`, and `string`
* Lambda expressions and functions
* Collection data structures like `list`, `tuple`, `map`, and `set`
* Enum types
* Classes and inheritance
* A set of built-in functions
* Basic control flow structures
* Other keywords and operators

## Specification

The syntax of `mini` is similar to the [ECMAScript specification](https://tc39.es/ecma262/), but not identical.

### Primitive data types

There are three primitive data types in `mini`:
* `number` - Represents both floating point and integer numbers
    * Arithmetic operators: `+`, `-`, `*`, `/`, `%` (modulo)
    * Comparison operators: `==`, `!=`, `<`, `<=`, `>`, `>=`
    * Examples: `21`, `4.2`, `-3`, `-3.5`
* `boolean` - Represents logical `true` or `false`
    * Logical operators: `&` (and), `|` (or), `!` (not)
    * Comparison operators: `==`
    * Examples: `true`, `false`
* `string` - Represents a sequence of characters, or a single character
    * Arithmetic operators: `+` (concatenation)
    * Comparison operators: `==`, `!=`
    * Examples: `"hello"`, `'world'`, `"a"`, `'b'`


### Variable declaration
A variable declaration is the same as an assignment, but if the variable is not already declared, it is automatically declared.

```js
x = 10
```

Multiple variables can be declared with the same value in a single statement.

```js
x = y = z = 10
```

Or multiple variables can be declared with different values on a single line, must be separated by whitespace.

```js
x = 10  y = 20  z = 30
```

### Lambda expressions

Lambdas are declared with the `=>` operator.
The left hand side of the `=>` is the parameter-list tuple, and the right hand side is the function body (A single expression or block).

```js
(x, y) => x + y
```

Functions can be declared by assigning a lambda expression to a variable.

```js
add = (x, y) => x + y
add(1, 2)
```

Empty parameter-list lambdas can be declared with an empty tuple. Used for generator and supplier functions.

```js
() => 42
```

It is also possible to write immediately invoked function expressions (IIFE) that runs as soon as it is defined.

```js
(() => "IIFE")()
```

### Collection data structures

Primitive data types are useful, but limiting on their own. `mini` has a number of data structures that can be used to store and manipulate collections of data.
* `list` - An ordered collection of values, where each value can be accessed by index. Elements are stored in the order they are declared.
    * Examples:
        * `[1, 2, 3]` - A list of three integers
        * `[true, false, 'hello', 'world']` - Mixed types
        * `[]` - An empty list
    * Methods:
        * `list.length` - The number of values in the list
        * `list[index]` - The value at the given index
        * `list.push(value)` - Adds a value to the end of the list
        * `list.pop()` - Removes and returns the last value in the list
        * `list.unshift(value)` - Adds a value to the beginning of the list
        * `list.shift()` - Removes and returns the first value in the list
        * `list.splice(start, deleteCount, ...values)` - Removes values from the list and returns them
        * `list.map(fn)` - Returns a new list with the values transformed by the given function
        * `list.filter(fn)` - Returns a new list with the values filtered by the given function
        * `list.reduce(fn, initialValue)` - Returns a single value by combining the values in the list
        * `list.indexOf(value)` - Returns the index of the given value, or `-1` if the value is not in the list
        * `list.lastIndexOf(value)` - Returns the index of the last given value, or `-1` if the value is not in the list
        * `list.join(separator)` - Returns a string with the values in the list separated by the given separator
        * `list.concat(...lists)` - Returns a new list with the values from the given lists
* `tuple` - An ordered collection of values, where each value can be accessed by index.
    * Examples:
        * `(1, 2, 3)` - A tuple of three integers
        * `('hello', 'world')` - A tuple of two strings
        * `()` - An empty tuple, or `unit`. **This should be treated the same as `null` in other languages.**
    * Methods:
        * `tuple.length` - The number of values in the tuple
        * `tuple[index]` - The value at the given index
* `map` - A disorderly collection of hashed key-value pairs, where each key can be accessed by index.
    * Examples:
        * `#{a: 1, b: 2, c: 3}` - A map of three key-value pairs
        * `#{0: 1, 1: 2, 2: 3}` - A map with numeric keys
        * `#{'hello world': 'hello', 'goodbye world': 'goodbye'}` - A map with string keys
        * `#{}` - An empty map
    * Methods:
        * `map[key]` - The value associated with the given key
        * `map.<key>` - The value associated with the given key, ie. `map.abc` is equivalent to `map['abc']`
        * `map.has(key)` - Returns `true` if the map contains the given key
        * `map.delete(key)` - Removes the value associated with the given key
        * `map.clear()` - Removes all key-value pairs from the map
        * `map.keys()` - Returns a new list with the keys in the map
        * `map.values()` - Returns a new list with the values in the map
        * `map.entries()` - Returns a new list with the key-value pairs in the map
* `set` - A disorderly collection of unique values.
    * Examples:
        * `set(1, 2, 3)` - Initialize a set with three unique values.
        * `set()` - The empty set.
    * `set.length` - The number of values in the set
    * `set.has(value)` - Returns `true` if the set contains the given value
    * `set.add(value)` - Adds the given value to the set
    * `set.delete(value)` - Removes the given value from the set
    * `set.clear()` - Removes all values from the set
    * `set.values()` - Returns a new list with the values in the set

### Enums

`mini` supports Rust-like enums.

```fs
enum Optional {
    Some(value),
    None
}

x = Optional.Some(42)
y = Optional.None
z = Optional.Some([1, 2, 3])
```

All identifiers in an enum value argument list must be unique. The values are assigned to the identifiers in the order they are declared and are dynamically typed.

### Classes

```ts
class Animal {
    constructor = (name) => #{
        name: name
    }

    speak = (this) => {
        return "{this.name} makes a noise."
    }
}
```

`mini` also supports basic inheritance.

```ts
class Dog: Animal {
    speak = (this) => {
        return "{this.speak()} Woof!"
    }
}
```


### Built-in functions

There are a number of built-in functions that can be used in `mini`:
* `print` - Prints a string to the console
    * Examples:
        * `print('hello')`
        * `print("hello", "world")`
        * `print(1, 2, 3)`
* `input` - Gets a string from the console
    * Examples:
        * `input()`
        * `input("Enter your name: ")`

There are also a number of helper functions to convert values between different types.
* `string` - String representation of a given value
    * Examples:
        * `string([1, 2, 3])`
        * `string(1.23)`
        * `string(true)`
        * `string(#{'a': 1, 'b': 2})`
        * `string("hello")`
* `number` - Integer representation of a given value
    * Examples:
        * `number('1')`
        * `number(1.23)`
        * `number(true)` - Returns `1`
        * `number(#{'a': 1, 'b': 2})` - Fails with an error
        * `number("hello")` - Fails with an error
* `boolean` - Boolean representation of a given value
    * Examples:
        * `boolean('1')` - Returns `true`
        * `boolean(1.23)` - Returns `true`
        * `boolean(0)` - Returns `false`
        * `boolean(true)` - Returns `true`
        * `boolean("")` - Returns `false`
        * `boolean(#{'a': 1, 'b': 2})` - Returns `true`
        * `boolean("hello")` - Returns `true`

### Control flow structures

There are three control flow structures in `mini`:
* `if` - If-then-else statement
* `match` - Pattern matching statement
* `for` - For-loop
* `while` - While-loop
* `break` - Break out of a loop
* `continue` - Continue to the next iteration of a loop
* `return` - Return from a function, last expression in a block is implicitly returned

Below are examples of each control flow structure.

> **`if` statement**
>
> The `if` statement is used to execute and return the value of a block of code or a single expression if a condition guard is true.

The guard is an expression directly following the `if` keyword, surrounding parentheses are optional. After that, a block of code or a single expression is specified.

```js
if x == 1 "one"
```

The example above returns the string `"one"` if the condition `x == 1` is true.

```js
if x % 2 == 0 {
    x *= 2
    return x + 1
}
```

The example above returns the value of `x * 2 + 1` if `x` is even.

If statements also has the power to pattern match on values using the `is` operator.

> **`if-else` statement**
>
> The `if-else` statement is used to execute and return the value of different blocks of code or single expressions depending on the value of a condition guard.

The code below is a short implementation of the absolute value function `|x|`.

```js
if x > 0 x
else -x
```

> **`else if` statement**
>
> The `else if` statements can be used to add additional conditions to an `if-else` statement.

```fs
if x >= 10 "ten or more"
else if x >= 5 "five or more"
else if x >= 1 "one or more"
else "none"
```

> **`match` statement**
>
> The `match` statement matches a value against a set of patterns, and returns the value of the first pattern that matches.

```fs
match x
    1 => "one"
    2 => "two"
    _ => "many"
```

One could think of match as many `if x is p` statements combined into a single statement.

A match case can also have a guard using the `if` keyword, which ensures that the pattern on the left hand side also satesfies a logical condition on the right hand side, before evaluating the matching case expression.

```fs
match x
    number(n) if n > 0 => "positive"
    number(n) if n < 0 => "negative"
    number(n) if n == 0 => "zero"
    _ => "not a number"
```


### Other keywords and operators

Other than the operators and keywords listed above, there are a number of other keywords and operators that can be used in `mini`.
* `is` - Used to match values against patterns and bind them to variables
* `in` - Used to check if a value is in a set of values

> **`is` keyword**
>
> The `is` keyword is used to match values against patterns and bind them to variables.

Use `is` in an if-else statement to pattern match on values and change the control flow of the program depending on the match result.

```ts
if x is number "number"
else if x is string "string"
else if x is boolean "boolean"
else "unknown"
```

Or more specifically, get the type of the value and bind it to a variable.

```ts
if x is number(n) "number: " + n
else if x is string(s) "string: " + s
else if x is boolean(b) "boolean: " + b
else "unknown: " + x
```

Can be used to handle optional values.

```fs
if x is Optional.Some(v) "some: " + v
else "none"
```

Or match on data types.

```ts
if l is [head | tail] "list: " + head + " " + tail
else 
```

> **`in` keyword**
>
> The `in` keyword is used to check if a value is in a set of values.

Check if a value is in a list.

```ts
if x in [1, 2, 3] "in list"
else "not in list"
```

Check if a value is in a range.

```ts
if x in 1..10 "in range"
else "not in range"
```

Check if value is a key in a map. If `x` would be `2` for example, `x` would be in the map and the condition would be true.

```ts
if x in {1: "one", 2: "two", 3: "three"} "in map"
else "not in map"
```

Check if a value is in a tuple.

```ts
if x in (1, 2, 3) "in tuple"
else "not in tuple"
```