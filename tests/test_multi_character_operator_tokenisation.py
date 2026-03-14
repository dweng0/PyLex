"""
Tests for the "Multi-character operator tokenisation" feature.
"""

import json
import subprocess
import sys
import os


def test_equality_operator_is_tokenised_as_a_single_token():
    """
    Scenario: Equality operator is tokenised as a single token
    
    Given a source file containing the equality operator "=="
    When I run the tokenizer with a lexer that defines operator tokens
    Then "==" appears as a single token with type "operator"
    And it is not split into two separate "=" tokens
    """
    # Create a test file with the equality operator
    test_file = "tests/fixtures/equality_operator.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('if x == 5:\n    pass\n')
    
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
    
    # Verify "==" appears as a single operator token
    found_equality = False
    for token in tokens:
        if token.get("value") == "==" and token.get("type") == "operator":
            found_equality = True
            break
    
    assert found_equality, f"Expected an operator token for '==' in output. Got: {tokens}"
    
    # Verify it's not split into two "=" tokens
    # Count consecutive "=" tokens - there should be none
    for i in range(len(tokens) - 1):
        if tokens[i].get("value") == "=" and tokens[i+1].get("value") == "=":
            raise AssertionError(f"Found two consecutive '=' tokens instead of '==': {tokens}")


def test_arrow_operator_is_tokenised_as_a_single_token():
    """
    Scenario: Arrow operator is tokenised as a single token
    
    Given a source file containing the arrow operator "=>"
    When I run the tokenizer with a lexer that defines operator tokens
    Then "=>" appears as a single token with type "operator"
    """
    # Create a test file with the arrow operator (JavaScript)
    test_file = "tests/fixtures/arrow_operator_test.js"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('const fn = (x) => x * 2;\n')
    
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
    
    # Verify "=>" appears as a single operator token
    found_arrow = False
    for token in tokens:
        if token.get("value") == "=>" and token.get("type") == "operator":
            found_arrow = True
            break
    
    assert found_arrow, f"Expected an operator token for '=>' in output. Got: {tokens}"


def test_compound_assignment_operators_are_tokenised_as_single_tokens():
    """
    Scenario: Compound assignment operators are tokenised as single tokens
    
    Given a source file containing compound assignment operators like "+=" or "-="
    When I run the tokenizer with a lexer that defines operator tokens
    Then each compound operator appears as a single token with type "operator"
    """
    # Create a test file with compound assignment operators
    test_file = "tests/fixtures/compound_assignment.py"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('x += 1\ny -= 2\nz *= 3\n')
    
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
    
    # Verify compound operators appear as single tokens
    found_plus_eq = False
    found_minus_eq = False
    found_mult_eq = False
    
    for token in tokens:
        if token.get("value") == "+=" and token.get("type") == "operator":
            found_plus_eq = True
        if token.get("value") == "-=" and token.get("type") == "operator":
            found_minus_eq = True
        if token.get("value") == "*=" and token.get("type") == "operator":
            found_mult_eq = True
    
    assert found_plus_eq, f"Expected an operator token for '+=' in output. Got: {tokens}"
    assert found_minus_eq, f"Expected an operator token for '-=' in output. Got: {tokens}"
    assert found_mult_eq, f"Expected an operator token for '*=' in output. Got: {tokens}"
