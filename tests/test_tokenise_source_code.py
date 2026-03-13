"""
Tests for the "Tokenise source code" feature.
"""

import json
import subprocess
import sys
import os


def test_tokenise_a_python_hello_world_file():
    """
    Scenario: Tokenise a Python hello-world file
    
    Given a Python source file and the Python lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "print"
    """
    # Create a temporary Python hello-world file
    test_file = "tests/fixtures/python_hello.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('print("Hello, World!")\n')
    
    # Run the tokenizer
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    # Check exit code
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    # Parse the output as JSON
    tokens = json.loads(result.stdout)
    
    # Verify it's a list (JSON array)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    # Verify output contains a keyword token for "print"
    found_print_keyword = False
    for token in tokens:
        if token.get("value") == "print" and token.get("type") == "keyword":
            found_print_keyword = True
            break
    
    assert found_print_keyword, f"Expected a keyword token for 'print' in output. Got: {tokens}"


def test_tokenise_a_javascript_hello_world_file():
    """
    Scenario: Tokenise a JavaScript hello-world file
    
    Given a JavaScript source file and the JavaScript lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "function"
    """
    test_file = "tests/fixtures/javascript_hello.js"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('function hello() { console.log("Hello"); }\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/javascript.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    found_function_keyword = False
    for token in tokens:
        if token.get("value") == "function" and token.get("type") == "keyword":
            found_function_keyword = True
            break
    
    assert found_function_keyword, f"Expected a keyword token for 'function' in output. Got: {tokens}"


def test_tokenise_a_typescript_hello_world_file():
    """
    Scenario: Tokenise a TypeScript hello-world file
    
    Given a TypeScript source file and the TypeScript lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "function"
    """
    test_file = "tests/fixtures/typescript_hello.ts"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('function hello(): void { console.log("Hello"); }\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/typescript.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    found_function_keyword = False
    for token in tokens:
        if token.get("value") == "function" and token.get("type") == "keyword":
            found_function_keyword = True
            break
    
    assert found_function_keyword, f"Expected a keyword token for 'function' in output. Got: {tokens}"


def test_tokenise_a_rust_hello_world_file():
    """
    Scenario: Tokenise a Rust hello-world file
    
    Given a Rust source file and the Rust lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "fn"
    """
    test_file = "tests/fixtures/rust_hello.rs"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('fn main() { println!("Hello"); }\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/rust.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    found_fn_keyword = False
    for token in tokens:
        if token.get("value") == "fn" and token.get("type") == "keyword":
            found_fn_keyword = True
            break
    
    assert found_fn_keyword, f"Expected a keyword token for 'fn' in output. Got: {tokens}"


def test_tokenise_a_cplusplus_hello_world_file():
    """
    Scenario: Tokenise a C++ hello-world file
    
    Given a C++ source file and the C++ lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "int"
    """
    test_file = "tests/fixtures/cplusplus_hello.cpp"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('int main() { return 0; }\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/cpp.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    found_int_keyword = False
    for token in tokens:
        if token.get("value") == "int" and token.get("type") == "keyword":
            found_int_keyword = True
            break
    
    assert found_int_keyword, f"Expected a keyword token for 'int' in output. Got: {tokens}"


def test_tokenise_a_fortran_hello_world_file():
    """
    Scenario: Tokenise a Fortran hello-world file
    
    Given a Fortran source file and the Fortran lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And the output contains a keyword token for "program"
    """
    test_file = "tests/fixtures/fortran_hello.f"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('program hello\n  print *, "Hello"\nend program hello\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/fortran.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    found_program_keyword = False
    for token in tokens:
        if token.get("value") == "program" and token.get("type") == "keyword":
            found_program_keyword = True
            break
    
    assert found_program_keyword, f"Expected a keyword token for 'program' in output. Got: {tokens}"


def test_tokenise_a_vyper_hello_world_file():
    """
    Scenario: Tokenise a Vyper hello-world file
    
    Given a Vyper source file and the Vyper lexer YAML
    When I run the tokenizer
    Then I receive a JSON array of tokens
    And every token has a non-empty "type" and "value"
    """
    test_file = "tests/fixtures/vyper_hello.vy"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('@external\ndef hello():\n    pass\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/vyper.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    # Verify every token has non-empty type and value
    for i, token in enumerate(tokens):
        assert token.get("type"), f"Token {i} has empty or missing 'type': {token}"
        assert token.get("value"), f"Token {i} has empty or missing 'value': {token}"
