"""
Tests for the "Number literal tokenisation" feature.
"""

import json
import subprocess
import sys
import os


def test_integer_literals_are_tokenised_as_number_tokens():
    """
    Scenario: Integer literals are tokenised as number tokens
    
    Given a source file containing an integer literal
    When I run the tokenizer with a lexer that defines number token patterns
    Then the integer appears as a token with type "number"
    """
    # Create a test file with an integer literal
    test_file = "tests/fixtures/integer_literal_test.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('x = 42\n')
    
    # Run the tokenizer with Python lexer
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
    
    # Verify "42" appears as a number token
    found_42 = False
    for token in tokens:
        if token.get("value") == "42" and token.get("type") == "number":
            found_42 = True
            break
    
    assert found_42, f"Expected a number token for '42' in output. Got: {tokens}"


def test_float_literals_are_tokenised_as_number_tokens():
    """
    Scenario: Float literals are tokenised as number tokens
    
    Given a source file containing a float literal
    When I run the tokenizer with a lexer that defines number token patterns
    Then the float appears as a token with type "number"
    """
    # Create a test file with a float literal
    test_file = "tests/fixtures/float_literal_test.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('x = 3.14\n')
    
    # Run the tokenizer with Python lexer
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
    
    # Verify "3.14" appears as a number token
    found_float = False
    for token in tokens:
        if token.get("value") == "3.14" and token.get("type") == "number":
            found_float = True
            break
    
    assert found_float, f"Expected a number token for '3.14' in output. Got: {tokens}"


def test_hexadecimal_literals_are_tokenised_as_number_tokens():
    """
    Scenario: Hexadecimal literals are tokenised as number tokens
    
    Given a source file containing a hexadecimal literal
    When I run the tokenizer with a lexer that defines number token patterns
    Then the hex literal appears as a token with type "number"
    """
    # Create a test file with a hexadecimal literal
    test_file = "tests/fixtures/hex_literal_test.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('x = 0xFF\n')
    
    # Run the tokenizer with Python lexer
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
    
    # Verify "0xFF" appears as a number token
    found_hex = False
    for token in tokens:
        if token.get("value") == "0xFF" and token.get("type") == "number":
            found_hex = True
            break
    
    assert found_hex, f"Expected a number token for '0xFF' in output. Got: {tokens}"
