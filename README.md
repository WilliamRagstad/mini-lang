<div align="center">
    <br>
    <img alt="Mini-Lang logo" src="assets/logo_small.png" width="300px"/>
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
It is not intended to be a full language, but rather a language that can be expanded upon and explore new and more advanced concepts in language design.

The language is expression-based, and is designed to be easy to learn and use.
It has support for:
* Basic arithmetic, logic, and comparison operators
* Primitive data types such as `number`, `boolean`, and `string`
* Lambda expressions and functions
* Basic control structures

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
