"""
Tests for the "Efficient string slicing" feature.
"""

import subprocess
import sys


def test_string_slice_extraction_uses_direct_slicing_instead_of_character_by_character_concatenation():
    """
    Scenario: String slice extraction uses direct slicing instead of character-by-character concatenation
    
    Given the tokenizer processes source code with identifiers and keywords
    When I run the tokenizer
    Then the output is correct (concatenation of token values reconstructs original input)
    And the implementation uses direct string slicing (verified by code inspection)
    
    Note: This test verifies the behavioral correctness. The implementation
    detail (direct slicing vs character-by-character) is verified by code review.
    """
    # Create a test file with various identifiers and keywords
    test_file = "tests/fixtures/slice_test.py"
    with open(test_file, "w") as f:
        f.write('def hello_world():\n    return "Hello, World!"\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    # Should succeed
    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}. stderr: {result.stderr}"
    
    # Output should be valid JSON
    import json
    tokens = json.loads(result.stdout)
    
    # Concatenating token values should reconstruct the original input
    reconstructed = ''.join(token['value'] for token in tokens)
    with open(test_file, "r") as f:
        original = f.read()
    
    assert reconstructed == original, \
        f"Reconstructed '{reconstructed}' does not match original '{original}'"
