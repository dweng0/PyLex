# BDD Status

Checked 28 scenario(s) across 22 test file(s).


## Feature: Tokenise source code

- [ ] UNCOVERED: Tokenise a Python hello-world file
- [ ] UNCOVERED: Tokenise a JavaScript hello-world file
- [ ] UNCOVERED: Tokenise a TypeScript hello-world file
- [ ] UNCOVERED: Tokenise a Rust hello-world file
- [ ] UNCOVERED: Tokenise a C++ hello-world file
- [ ] UNCOVERED: Tokenise a Fortran hello-world file
- [ ] UNCOVERED: Tokenise a Vyper hello-world file

## Feature: JSON output format

- [x] Output is a valid JSON array
- [ ] UNCOVERED: Token types are non-empty strings
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

- [ ] UNCOVERED: Missing command-line arguments prints usage and exits non-zero
- [x] Input file not found exits with a clear error message
- [x] Invalid YAML lexer config exits with a clear error message

## Feature: Lexer schema validation

- [x] Valid lexer YAML passes validation
- [x] Lexer YAML missing required field fails validation
- [x] Lexer YAML with a token missing both value and pattern fails validation
- [x] All bundled lexer files pass validation

## Feature: Custom lexer configuration

- [x] A custom lexer tokenises a simple DSL

---
**19/28 scenarios covered.**

9 scenario(s) need tests:
- Tokenise a Python hello-world file
- Tokenise a JavaScript hello-world file
- Tokenise a TypeScript hello-world file
- Tokenise a Rust hello-world file
- Tokenise a C++ hello-world file
- Tokenise a Fortran hello-world file
- Tokenise a Vyper hello-world file
- Token types are non-empty strings
- Missing command-line arguments prints usage and exits non-zero
