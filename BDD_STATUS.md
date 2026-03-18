# BDD Status

Checked 49 scenario(s) across 41 test file(s).


## Feature: Tokenise source code

- [x] Tokenise a Python hello-world file
- [x] Tokenise a JavaScript hello-world file
- [x] Tokenise a TypeScript hello-world file
- [x] Tokenise a Rust hello-world file
- [x] Tokenise a C++ hello-world file
- [x] Tokenise a Fortran hello-world file
- [x] Tokenise a Vyper hello-world file

## Feature: JSON output format

- [x] Output is a valid JSON array
- [x] Token types are non-empty strings
- [x] Concatenating token values reconstructs the original input
- [x] Unrecognised characters are reported on stderr not stdout

## Feature: Token type identification

- [x] Keywords are identified as keyword tokens
- [x] Identifiers are identified as identifier tokens
- [x] Whitespace is preserved as whitespace tokens
- [x] String literals are identified as string literal tokens
- [x] Operators are identified as operator tokens
- [x] Keywords are not misidentified as identifiers

## Feature: Comprehensive language tokenisation

- [x] Tokenise a Python file with function definition and control flow
- [x] Tokenise a JavaScript file with variable declarations and arrow functions
- [x] Tokenise a Rust file with struct and impl definitions

## Feature: CLI error handling

- [x] Missing command-line arguments prints usage and exits non-zero
- [x] Input file not found exits with a clear error message
- [x] Invalid YAML lexer config exits with a clear error message

## Feature: Lexer schema validation

- [x] Valid lexer YAML passes validation
- [x] Lexer YAML missing required field fails validation
- [x] Lexer YAML with a token missing both value and pattern fails validation
- [x] All bundled lexer files pass validation

## Feature: Custom lexer configuration

- [x] A custom lexer tokenises a simple DSL

## Feature: Comment tokenisation

- [x] Single-line comments are tokenised as comment tokens
- [x] Multi-line comments are tokenised as comment tokens

## Feature: Import statement tokenisation

- [x] Python import statement is tokenised correctly
- [x] JavaScript import statement is tokenised correctly
- [x] Rust use statement is tokenised correctly

## Feature: Multi-character operator tokenisation

- [x] Equality operator is tokenised as a single token
- [x] Arrow operator is tokenised as a single token
- [x] Compound assignment operators are tokenised as single tokens

## Feature: Number literal tokenisation

- [x] Integer literals are tokenised as number tokens
- [x] Float literals are tokenised as number tokens
- [x] Hexadecimal literals are tokenised as number tokens

## Feature: Empty input handling

- [x] Empty file produces an empty token array
- [x] Whitespace-only file produces only whitespace tokens

## Feature: Duplicate token deduplication

- [x] Duplicate value-based tokens are rejected during validation
- [x] Bundled lexers contain no duplicate token values

## Feature: Regex pattern precompilation

- [x] Patterns are compiled once before tokenisation begins
- [x] Large file tokenisation completes within a reasonable time

## Feature: Efficient string slicing

- [x] String slice extraction uses direct slicing instead of character-by-character concatenation

## Feature: CLI error messages

- [x] File not found produces a clean error message without a traceback
- [x] Invalid YAML produces a clean error message without a traceback
- [x] Unreadable file produces a clean error message without a traceback

---
**49/49 scenarios covered.**
