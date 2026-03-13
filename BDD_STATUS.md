# BDD Status

Checked 28 scenario(s) across 0 test file(s).


## Feature: Tokenise source code

- [ ] UNCOVERED: Tokenise a Python hello-world file
- [ ] UNCOVERED: Tokenise a JavaScript hello-world file
- [ ] UNCOVERED: Tokenise a TypeScript hello-world file
- [ ] UNCOVERED: Tokenise a Rust hello-world file
- [ ] UNCOVERED: Tokenise a C++ hello-world file
- [ ] UNCOVERED: Tokenise a Fortran hello-world file
- [ ] UNCOVERED: Tokenise a Vyper hello-world file

## Feature: JSON output format

- [ ] UNCOVERED: Output is a valid JSON array
- [ ] UNCOVERED: Token types are non-empty strings
- [ ] UNCOVERED: Concatenating token values reconstructs the original input
- [ ] UNCOVERED: Unrecognised characters are reported on stderr not stdout

## Feature: Token type identification

- [ ] UNCOVERED: Keywords are identified as keyword tokens
- [ ] UNCOVERED: Identifiers are identified as identifier tokens
- [ ] UNCOVERED: Whitespace is preserved as whitespace tokens
- [ ] UNCOVERED: String literals are identified as string literal tokens
- [ ] UNCOVERED: Operators are identified as operator tokens
- [ ] UNCOVERED: Keywords are not misidentified as identifiers

## Feature: Comprehensive language tokenisation

- [ ] UNCOVERED: Tokenise a Python file with function definition and control flow
- [ ] UNCOVERED: Tokenise a JavaScript file with variable declarations and arrow functions
- [ ] UNCOVERED: Tokenise a Rust file with struct and impl definitions

## Feature: CLI error handling

- [ ] UNCOVERED: Missing command-line arguments prints usage and exits non-zero
- [ ] UNCOVERED: Input file not found exits with a clear error message
- [ ] UNCOVERED: Invalid YAML lexer config exits with a clear error message

## Feature: Lexer schema validation

- [ ] UNCOVERED: Valid lexer YAML passes validation
- [ ] UNCOVERED: Lexer YAML missing required field fails validation
- [ ] UNCOVERED: Lexer YAML with a token missing both value and pattern fails validation
- [ ] UNCOVERED: All bundled lexer files pass validation

## Feature: Custom lexer configuration

- [ ] UNCOVERED: A custom lexer tokenises a simple DSL

---
**0/28 scenarios covered.**

28 scenario(s) need tests:
- Tokenise a Python hello-world file
- Tokenise a JavaScript hello-world file
- Tokenise a TypeScript hello-world file
- Tokenise a Rust hello-world file
- Tokenise a C++ hello-world file
- Tokenise a Fortran hello-world file
- Tokenise a Vyper hello-world file
- Output is a valid JSON array
- Token types are non-empty strings
- Concatenating token values reconstructs the original input
- Unrecognised characters are reported on stderr not stdout
- Keywords are identified as keyword tokens
- Identifiers are identified as identifier tokens
- Whitespace is preserved as whitespace tokens
- String literals are identified as string literal tokens
- Operators are identified as operator tokens
- Keywords are not misidentified as identifiers
- Tokenise a Python file with function definition and control flow
- Tokenise a JavaScript file with variable declarations and arrow functions
- Tokenise a Rust file with struct and impl definitions
- Missing command-line arguments prints usage and exits non-zero
- Input file not found exits with a clear error message
- Invalid YAML lexer config exits with a clear error message
- Valid lexer YAML passes validation
- Lexer YAML missing required field fails validation
- Lexer YAML with a token missing both value and pattern fails validation
- All bundled lexer files pass validation
- A custom lexer tokenises a simple DSL
