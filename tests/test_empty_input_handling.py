"""
Tests for the "Empty input handling" feature.

Coverage markers (normalized scenario names for check_bdd_coverage.py):
- whitespaceonly_file_produces_only_whitespace_tokens
"""

import json
import subprocess
import sys
import os


def test_whitespace_only_file_produces_only_whitespace_tokens():
    """
    Scenario: Whitespace-only file produces only whitespace tokens
    
    Given a source file containing only whitespace characters (spaces, tabs, newlines)
    When I run the tokenizer with a lexer that defines whitespace token patterns
    Then the output contains only tokens with type "whitespace"
    And the concatenation of all token values reconstructs the original input
    """
    # Create a test file with only whitespace
    test_file = "tests/fixtures/whitespace_only_test.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('   \t\n  \n')
    
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
    
    # Verify all tokens are whitespace tokens
    for i, token in enumerate(tokens):
        assert token.get("type") == "whitespace", f"Token {i} should be whitespace but got type '{token.get('type')}': {token}"
    
    # Verify concatenation reconstructs the original input
    reconstructed = "".join(token.get("value", "") for token in tokens)
    with open(test_file, "r") as f:
        original = f.read()
    assert reconstructed == original, f"Reconstructed '{reconstructed}' != original '{original}'"
