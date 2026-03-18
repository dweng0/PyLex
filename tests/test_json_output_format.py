"""
Tests for the "JSON output format" feature.

Coverage markers (normalized scenario names for check_bdd_coverage.py):
- token_types_are_nonempty_strings
"""

import json
import subprocess
import sys
import os


def test_output_is_a_valid_json_array():
    """
    Scenario: Output is a valid JSON array
    
    Given any supported source file and its lexer YAML
    When I run the tokenizer
    Then stdout is parseable as a JSON array
    And each element has a "value" field and a "type" field
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Test with Python
    test_file = "tests/fixtures/json_test.py"
    with open(test_file, "w") as f:
        f.write('x = 1\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    # Verify stdout is parseable as a JSON array
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    # Verify each element has "value" and "type" fields
    for i, token in enumerate(tokens):
        assert "value" in token, f"Token {i} missing 'value' field: {token}"
        assert "type" in token, f"Token {i} missing 'type' field: {token}"


def test_token_types_are_non_empty_strings():
    """
    Scenario: Token types are non-empty strings
    
    Given any supported source file and its lexer YAML
    When I run the tokenizer
    Then every token has a non-empty string "type"
    And every token has a non-empty string "value"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/token_types_test.py"
    with open(test_file, "w") as f:
        f.write('def foo(): pass\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    for i, token in enumerate(tokens):
        assert isinstance(token.get("type"), str), f"Token {i} 'type' is not a string: {token}"
        assert token.get("type"), f"Token {i} has empty 'type': {token}"
        assert isinstance(token.get("value"), str), f"Token {i} 'value' is not a string: {token}"
        assert token.get("value"), f"Token {i} has empty 'value': {token}"


def test_concatenating_token_values_reconstructs_the_original_input():
    """
    Scenario: Concatenating token values reconstructs the original input
    
    Given any supported source file and its lexer YAML
    When I run the tokenizer
    Then concatenating all token "value" fields produces the original source file content
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    original_content = 'x = 42\n'
    test_file = "tests/fixtures/reconstruct_test.py"
    with open(test_file, "w") as f:
        f.write(original_content)
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    # Concatenate all token values
    reconstructed = "".join(token["value"] for token in tokens)
    
    assert reconstructed == original_content, f"Reconstructed '{reconstructed}' != original '{original_content}'"


def test_unrecognised_characters_are_reported_on_stderr_not_stdout():
    """
    Scenario: Unrecognised characters are reported on stderr not stdout
    
    Given a source file containing a character not matched by any token rule
    When I run the tokenizer
    Then stdout remains a valid JSON array
    And the warning about the unrecognised character appears on stderr
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a custom lexer without a catch-all pattern
    custom_lexer = "tests/fixtures/strict_lexer.yaml"
    with open(custom_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types: []
tokens:
  - type: identifier
    pattern: "[a-zA-Z_][a-zA-Z0-9_]*"
  - type: whitespace
    pattern: "\\\\s+"
""")
    
    # Create a file with a character that won't match (special char not in patterns)
    test_file = "tests/fixtures/unrecognised_test.input"
    with open(test_file, "w") as f:
        f.write('x@y\n')  # @ is not matched by identifier or whitespace patterns
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, custom_lexer],
        capture_output=True,
        text=True
    )
    
    # stdout should still be valid JSON
    try:
        tokens = json.loads(result.stdout)
        assert isinstance(tokens, list), "stdout should be a JSON array"
    except json.JSONDecodeError as e:
        raise AssertionError(f"stdout is not valid JSON: {result.stdout}") from e
    
    # stderr should contain a warning about the unrecognised character
    assert "could not determine" in result.stderr.lower() or "lexical" in result.stderr.lower(), \
        f"Expected warning about unrecognised character in stderr. Got: {result.stderr}"
