"""
Tests for the "Comprehensive language tokenisation" feature.
"""

import json
import subprocess
import sys
import os


def test_tokenise_a_python_file_with_function_definition_and_control_flow():
    """
    Scenario: Tokenise a Python file with function definition and control flow
    
    Given a Python source file containing a function definition and an if statement
    When I run the tokenizer with the Python lexer
    Then tokens include keywords "def", "if", and "return"
    And identifiers for the function name and variable names are present
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/python_comprehensive.py"
    with open(test_file, "w") as f:
        f.write("""def check_value(x):
    if x > 0:
        return True
    return False
""")
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    # Check for required keywords
    found_def = any(t.get("value") == "def" and t.get("type") == "keyword" for t in tokens)
    found_if = any(t.get("value") == "if" and t.get("type") == "keyword" for t in tokens)
    found_return = any(t.get("value") == "return" and t.get("type") == "keyword" for t in tokens)
    
    # Check for identifiers
    found_check_value = any(t.get("value") == "check_value" and t.get("type") == "identifier" for t in tokens)
    found_x = any(t.get("value") == "x" and t.get("type") == "identifier" for t in tokens)
    
    assert found_def, f"Expected 'def' keyword. Got: {tokens}"
    assert found_if, f"Expected 'if' keyword. Got: {tokens}"
    assert found_return, f"Expected 'return' keyword. Got: {tokens}"
    assert found_check_value, f"Expected 'check_value' identifier. Got: {tokens}"
    assert found_x, f"Expected 'x' identifier. Got: {tokens}"


def test_tokenise_a_javascript_file_with_variable_declarations_and_arrow_functions():
    """
    Scenario: Tokenise a JavaScript file with variable declarations and arrow functions
    
    Given a JavaScript source file containing "const", "let", and an arrow function
    When I run the tokenizer with the JavaScript lexer
    Then tokens include keywords "const" and "let"
    And the arrow function syntax is tokenised without errors
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/javascript_comprehensive.js"
    with open(test_file, "w") as f:
        f.write("""const x = 1;
let y = 2;
const add = (a, b) => a + b;
""")
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/javascript.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    # Check for required keywords
    found_const = any(t.get("value") == "const" and t.get("type") == "keyword" for t in tokens)
    found_let = any(t.get("value") == "let" and t.get("type") == "keyword" for t in tokens)
    
    assert found_const, f"Expected 'const' keyword. Got: {tokens}"
    assert found_let, f"Expected 'let' keyword. Got: {tokens}"


def test_tokenise_a_rust_file_with_struct_and_impl_definitions():
    """
    Scenario: Tokenise a Rust file with struct and impl definitions
    
    Given a Rust source file containing a struct and an impl block
    When I run the tokenizer with the Rust lexer
    Then tokens include keywords "struct" and "impl"
    And identifiers for the struct name are present
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/rust_comprehensive.rs"
    with open(test_file, "w") as f:
        f.write("""struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Point {
        Point { x, y }
    }
}
""")
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/rust.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    # Check for required keywords
    found_struct = any(t.get("value") == "struct" and t.get("type") == "keyword" for t in tokens)
    found_impl = any(t.get("value") == "impl" and t.get("type") == "keyword" for t in tokens)
    
    # Check for struct name identifier
    found_point = any(t.get("value") == "Point" and t.get("type") == "identifier" for t in tokens)
    
    assert found_struct, f"Expected 'struct' keyword. Got: {tokens}"
    assert found_impl, f"Expected 'impl' keyword. Got: {tokens}"
    assert found_point, f"Expected 'Point' identifier. Got: {tokens}"
