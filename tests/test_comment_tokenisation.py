"""
Tests for the "Comment tokenisation" feature.
"""

import json
import subprocess
import sys
import os


def test_single_line_comments_are_tokenised_as_comment_tokens():
    """
    Scenario: Single-line comments are tokenised as comment tokens
    
    Given a source file containing a single-line comment (e.g. "# hello" or "// hello")
    When I run the tokenizer with a lexer that defines a single-line comment pattern
    Then the comment text appears as a token with type "comment"
    And the concatenation of all token values reconstructs the original input
    """
    # Create a test file with a single-line comment
    test_file = "tests/fixtures/single_line_comment_test.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('x = 1  # this is a comment\n')
    
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
    
    # Verify the comment appears as a token with type "comment" or "single_line_comment"
    found_comment = False
    for token in tokens:
        token_type = token.get("type", "")
        if "comment" in token_type.lower():
            found_comment = True
            # Verify the token value contains the comment text
            assert "#" in token.get("value", ""), f"Comment token should contain '#': {token}"
            break
    
    assert found_comment, f"Expected a comment token in output. Got: {tokens}"
    
    # Verify concatenation reconstructs the original input
    reconstructed = "".join(token.get("value", "") for token in tokens)
    with open(test_file, "r") as f:
        original = f.read()
    assert reconstructed == original, f"Reconstructed '{reconstructed}' != original '{original}'"


def test_multi_line_comments_are_tokenised_as_comment_tokens():
    """
    Scenario: Multi-line comments are tokenised as comment tokens
    
    Given a source file containing a block comment (e.g. "/* ... */")
    When I run the tokenizer with a lexer that defines a multi-line comment pattern
    Then the entire block comment appears as a token with type "comment"
    And the concatenation of all token values reconstructs the original input
    """
    # Create a test file with a multi-line comment
    test_file = "tests/fixtures/multi_line_comment_test.js"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('/* this is\na multi-line\ncomment */\nvar x = 1;\n')
    
    # Run the tokenizer with JavaScript lexer
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/javascript.yaml"],
        capture_output=True,
        text=True
    )
    
    # Check exit code
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    # Parse the output as JSON
    tokens = json.loads(result.stdout)
    
    # Verify it's a list (JSON array)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    # Verify the multi-line comment appears as a token with type "comment" or "multi_line_comment"
    found_comment = False
    for token in tokens:
        token_type = token.get("type", "")
        if "comment" in token_type.lower():
            found_comment = True
            # Verify the token value contains the entire block comment
            value = token.get("value", "")
            assert "/*" in value and "*/" in value, f"Multi-line comment token should contain '/*' and '*/': {token}"
            break
    
    assert found_comment, f"Expected a comment token in output. Got: {tokens}"
    
    # Verify concatenation reconstructs the original input
    reconstructed = "".join(token.get("value", "") for token in tokens)
    with open(test_file, "r") as f:
        original = f.read()
    assert reconstructed == original, f"Reconstructed '{reconstructed}' != original '{original}'"
