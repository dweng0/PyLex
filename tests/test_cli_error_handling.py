"""
Tests for the "CLI error handling" feature.
"""

import subprocess
import sys
import os


def test_missing_command_line_arguments_prints_usage_and_exits_non_zero():
    """
    Scenario: Missing command-line arguments prints usage and exits non-zero
    
    Given I run the tokenizer with no arguments
    Then the exit code is non-zero
    And a usage message is printed to stderr
    """
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True
    )
    
    # Exit code should be non-zero
    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    # Usage message should be printed to stderr
    assert "usage" in result.stderr.lower() or "argument" in result.stderr.lower(), \
        f"Expected usage message in stderr. Got: {result.stderr}"


def test_input_file_not_found_exits_with_a_clear_error_message():
    """
    Scenario: Input file not found exits with a clear error message
    
    Given I run the tokenizer with a path to a file that does not exist
    Then the exit code is non-zero
    And an error message mentioning the missing file is printed to stderr
    """
    result = subprocess.run(
        [sys.executable, "main.py", "nonexistent_file.py", "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    # Exit code should be non-zero
    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    # Error message should mention the missing file
    assert "nonexistent_file" in result.stderr or "No such file" in result.stderr or "not found" in result.stderr.lower(), \
        f"Expected error message mentioning missing file. Got: {result.stderr}"


def test_invalid_yaml_lexer_config_exits_with_a_clear_error_message():
    """
    Scenario: Invalid YAML lexer config exits with a clear error message
    
    Given I run the tokenizer with a lexer config file containing invalid YAML
    Then the exit code is non-zero
    And an error message describing the YAML parse failure is printed to stderr
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create an invalid YAML file
    invalid_lexer = "tests/fixtures/invalid_lexer.yaml"
    with open(invalid_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " "
tokens:
  - type: identifier
    pattern: "[a-zA-Z]+"
  - this is invalid yaml: [unclosed
""")
    
    test_file = "tests/fixtures/test_input.txt"
    with open(test_file, "w") as f:
        f.write('hello')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, invalid_lexer],
        capture_output=True,
        text=True
    )
    
    # Exit code should be non-zero
    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    
    # Error message should describe the YAML parse failure
    assert "yaml" in result.stderr.lower() or "parse" in result.stderr.lower() or "error" in result.stderr.lower(), \
        f"Expected YAML parse error message. Got: {result.stderr}"
