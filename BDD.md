---
language: python
framework: none
build_cmd: python3 -m py_compile main.py tokenizer/tokenizer.py lexers/lexer.py validate.py hard_validate.py
test_cmd: python3 -m pytest tests/ -v
lint_cmd: echo 'lint not configured'
fmt_cmd: echo 'format not configured'
birth_date: 2026-03-13
---

You must only write code and tests that meet the features and scenarios of this behaviour driven development document.

System: A YAML-configured lexer (tokenizer) that converts source code files into a stream of typed JSON tokens. Language support is defined by YAML lexer files. The tokenizer is invoked from the command line and outputs a JSON array.

    Feature: Tokenise source code
        As a developer
        I want to tokenise source code using a YAML lexer config
        So that I can analyse or transform code programmatically

        Scenario: Tokenise a Python hello-world file
            Given a Python source file and the Python lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "print"

        Scenario: Tokenise a JavaScript hello-world file
            Given a JavaScript source file and the JavaScript lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "function"

        Scenario: Tokenise a TypeScript hello-world file
            Given a TypeScript source file and the TypeScript lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "function"

        Scenario: Tokenise a Rust hello-world file
            Given a Rust source file and the Rust lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "fn"

        Scenario: Tokenise a C++ hello-world file
            Given a C++ source file and the C++ lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "int"

        Scenario: Tokenise a Fortran hello-world file
            Given a Fortran source file and the Fortran lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And the output contains a keyword token for "program"

        Scenario: Tokenise a Vyper hello-world file
            Given a Vyper source file and the Vyper lexer YAML
            When I run the tokenizer
            Then I receive a JSON array of tokens
            And every token has a non-empty "type" and "value"

    Feature: JSON output format
        As a developer consuming PyLex output
        I want the tokenizer output to be valid, well-structured JSON
        So that I can parse and process it reliably

        Scenario: Output is a valid JSON array
            Given any supported source file and its lexer YAML
            When I run the tokenizer
            Then stdout is parseable as a JSON array
            And each element has a "value" field and a "type" field

        Scenario: Token types are non-empty strings
            Given any supported source file and its lexer YAML
            When I run the tokenizer
            Then every token has a non-empty string "type"
            And every token has a non-empty string "value"

        Scenario: Concatenating token values reconstructs the original input
            Given any supported source file and its lexer YAML
            When I run the tokenizer
            Then concatenating all token "value" fields produces the original source file content

        Scenario: Unrecognised characters are reported on stderr not stdout
            Given a source file containing a character not matched by any token rule
            When I run the tokenizer
            Then stdout remains a valid JSON array
            And the warning about the unrecognised character appears on stderr

    Feature: Token type identification
        As a developer
        I want source code tokens to be correctly classified by type
        So that I can distinguish keywords from identifiers, literals, and operators

        Scenario: Keywords are identified as keyword tokens
            Given a source file containing a language keyword
            When I run the tokenizer with the appropriate lexer
            Then the keyword appears as a token with type "keyword"

        Scenario: Identifiers are identified as identifier tokens
            Given a source file containing a user-defined name
            When I run the tokenizer with the appropriate lexer
            Then the name appears as a token with type "identifier"

        Scenario: Whitespace is preserved as whitespace tokens
            Given a source file containing spaces or newlines
            And the lexer YAML defines a whitespace token pattern
            When I run the tokenizer with the appropriate lexer
            Then whitespace appears as tokens with type "whitespace" in the output
            And whitespace is not silently discarded

        Scenario: String literals are identified as string literal tokens
            Given a source file containing a quoted string
            When I run the tokenizer with a lexer that defines a string_literal pattern
            Then the quoted string appears as a token with type "string_literal"

        Scenario: Operators are identified as operator tokens
            Given a source file containing operators such as "+" or "="
            When I run the tokenizer with a lexer that defines operator tokens
            Then each operator appears as a token with type "operator"

        Scenario: Keywords are not misidentified as identifiers
            Given a source file where a keyword appears adjacent to an identifier
            When I run the tokenizer with the appropriate lexer
            Then the keyword token has type "keyword" not "identifier"
            And the identifier token has type "identifier"

    Feature: Comprehensive language tokenisation
        As a developer
        I want each bundled lexer to handle common real-world code constructs
        So that the tokenizer is useful beyond hello-world examples

        Scenario: Tokenise a Python file with function definition and control flow
            Given a Python source file containing a function definition and an if statement
            When I run the tokenizer with the Python lexer
            Then tokens include keywords "def", "if", and "return"
            And identifiers for the function name and variable names are present

        Scenario: Tokenise a JavaScript file with variable declarations and arrow functions
            Given a JavaScript source file containing "const", "let", and an arrow function
            When I run the tokenizer with the JavaScript lexer
            Then tokens include keywords "const" and "let"
            And the arrow function syntax is tokenised without errors

        Scenario: Tokenise a Rust file with struct and impl definitions
            Given a Rust source file containing a struct and an impl block
            When I run the tokenizer with the Rust lexer
            Then tokens include keywords "struct" and "impl"
            And identifiers for the struct name are present

    Feature: CLI error handling
        As a developer running PyLex from the command line
        I want clear error messages when I misuse the tool
        So that I can quickly understand and fix the problem

        Scenario: Missing command-line arguments prints usage and exits non-zero
            Given I run the tokenizer with no arguments
            Then the exit code is non-zero
            And a usage message is printed to stderr

        Scenario: Input file not found exits with a clear error message
            Given I run the tokenizer with a path to a file that does not exist
            Then the exit code is non-zero
            And an error message mentioning the missing file is printed to stderr

        Scenario: Invalid YAML lexer config exits with a clear error message
            Given I run the tokenizer with a lexer config file containing invalid YAML
            Then the exit code is non-zero
            And an error message describing the YAML parse failure is printed to stderr

    Feature: Lexer schema validation
        As a lexer author
        I want invalid YAML lexer files to be rejected
        So that I can catch configuration mistakes early

        Scenario: Valid lexer YAML passes validation
            Given a correctly structured lexer YAML file
            When I run validate.py
            Then the exit code is 0
            And no errors are reported

        Scenario: Lexer YAML missing required field fails validation
            Given a lexer YAML file missing the "tokens" field
            When I run validate.py
            Then the exit code is non-zero
            And an error message describes the missing field

        Scenario: Lexer YAML with a token missing both value and pattern fails validation
            Given a lexer YAML file containing a token definition with neither "value" nor "pattern"
            When I run validate.py
            Then the exit code is non-zero
            And an error message describes the invalid token definition

        Scenario: All bundled lexer files pass validation
            Given all YAML files in the lexers/ directory
            When I run validate.py on each one
            Then every file passes validation with exit code 0

    Feature: Custom lexer configuration
        As a developer
        I want to write my own lexer YAML configuration
        So that I can tokenise languages or dialects not bundled with PyLex

        Scenario: A custom lexer tokenises a simple DSL
            Given a custom lexer YAML defining two token types and a simple input string
            When I run the tokenizer with that custom lexer
            Then the output contains tokens matching the custom definitions
            And no tokens from the built-in lexers appear in the output

    Feature: Comment tokenisation
        As a developer
        I want comments in source code to be tokenised correctly
        So that I can preserve or strip them in downstream tooling

        Scenario: Single-line comments are tokenised as comment tokens
            Given a source file containing a single-line comment (e.g. "# hello" or "// hello")
            When I run the tokenizer with a lexer that defines a single-line comment pattern
            Then the comment text appears as a token with type "comment"
            And the concatenation of all token values reconstructs the original input

        Scenario: Multi-line comments are tokenised as comment tokens
            Given a source file containing a block comment (e.g. "/* ... */")
            When I run the tokenizer with a lexer that defines a multi-line comment pattern
            Then the entire block comment appears as a token with type "comment"
            And the concatenation of all token values reconstructs the original input

    Feature: Import statement tokenisation
        As a developer
        I want import and use statements to be tokenised correctly
        So that I can analyse dependencies programmatically

        Scenario: Python import statement is tokenised correctly
            Given a Python source file containing "import os" and "from sys import path"
            When I run the tokenizer with the Python lexer
            Then "import" and "from" appear as keyword tokens
            And "os", "sys", and "path" appear as identifier tokens

        Scenario: JavaScript import statement is tokenised correctly
            Given a JavaScript source file containing an ES6 import statement
            When I run the tokenizer with the JavaScript lexer
            Then "import" and "from" appear as keyword tokens
            And the module name appears as a string literal token

        Scenario: Rust use statement is tokenised correctly
            Given a Rust source file containing a "use" declaration
            When I run the tokenizer with the Rust lexer
            Then "use" appears as a keyword token
            And the path components appear as identifier tokens

    Feature: Multi-character operator tokenisation
        As a developer
        I want multi-character operators to be tokenised as single tokens
        So that "==" is not split into two "=" tokens

        Scenario: Equality operator is tokenised as a single token
            Given a source file containing "=="
            When I run the tokenizer with a lexer that defines a "==" operator
            Then "==" appears as a single operator token
            And it is not split into two separate "=" tokens

        Scenario: Arrow operator is tokenised as a single token
            Given a source file containing "=>" or "->"
            When I run the tokenizer with a lexer that defines arrow operators
            Then the arrow appears as a single operator token

        Scenario: Compound assignment operators are tokenised as single tokens
            Given a source file containing "+=", "-=", or "*="
            When I run the tokenizer with a lexer that defines compound assignment operators
            Then each compound operator appears as a single operator token

    Feature: Number literal tokenisation
        As a developer
        I want numeric literals to be tokenised as number tokens
        So that I can distinguish them from identifiers and keywords

        Scenario: Integer literals are tokenised as number tokens
            Given a source file containing integer literals such as "42" and "0"
            When I run the tokenizer with a lexer that defines a number pattern
            Then each integer appears as a token with type "number"

        Scenario: Float literals are tokenised as number tokens
            Given a source file containing float literals such as "3.14" and "0.5"
            When I run the tokenizer with a lexer that defines a number pattern
            Then each float appears as a token with type "number"

        Scenario: Hexadecimal literals are tokenised as number tokens
            Given a source file containing hex literals such as "0xFF" and "0x1A2B"
            When I run the tokenizer with a lexer that defines a hex number pattern
            Then each hex literal appears as a token with type "number"

    Feature: Empty input handling
        As a developer
        I want the tokenizer to handle empty or whitespace-only files gracefully
        So that it does not crash on edge-case inputs

        Scenario: Empty file produces an empty token array
            Given an empty source file
            When I run the tokenizer
            Then the output is a valid JSON array
            And the array is empty

        Scenario: Whitespace-only file produces only whitespace tokens
            Given a source file containing only spaces and newlines
            When I run the tokenizer with a lexer that defines a whitespace pattern
            Then the output contains only whitespace tokens
            And the concatenation of token values equals the original input
