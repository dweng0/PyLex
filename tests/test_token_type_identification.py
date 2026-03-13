"""
Tests for the "Token type identification" feature.
"""

import json
import subprocess
import sys
import os


def test_keywords_are_identified_as_keyword_tokens():
    """
    Scenario: Keywords are identified as keyword tokens
    
    Given a source file containing a language keyword
    When I run the tokenizer with the appropriate lexer
    Then the keyword appears as a token with type "keyword"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/keyword_test.py"
    with open(test_file, "w") as f:
        f.write('def foo(): pass\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    found_def_keyword = False
    for token in tokens:
        if token.get("value") == "def" and token.get("type") == "keyword":
            found_def_keyword = True
            break
    
    assert found_def_keyword, f"Expected keyword token for 'def'. Got: {tokens}"


def test_identifiers_are_identified_as_identifier_tokens():
    """
    Scenario: Identifiers are identified as identifier tokens
    
    Given a source file containing a user-defined name
    When I run the tokenizer with the appropriate lexer
    Then the name appears as a token with type "identifier"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/identifier_test.py"
    with open(test_file, "w") as f:
        f.write('my_variable = 42\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    found_my_variable = False
    for token in tokens:
        if token.get("value") == "my_variable" and token.get("type") == "identifier":
            found_my_variable = True
            break
    
    assert found_my_variable, f"Expected identifier token for 'my_variable'. Got: {tokens}"


def test_whitespace_is_preserved_as_whitespace_tokens():
    """
    Scenario: Whitespace is preserved as whitespace tokens
    
    Given a source file containing spaces or newlines
    And the lexer YAML defines a whitespace token pattern
    When I run the tokenizer with the appropriate lexer
    Then whitespace appears as tokens with type "whitespace" in the output
    And whitespace is not silently discarded
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/whitespace_test.py"
    with open(test_file, "w") as f:
        f.write('x  =  42\n')  # Multiple spaces
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    found_whitespace = False
    for token in tokens:
        if token.get("type") == "whitespace":
            found_whitespace = True
            break
    
    assert found_whitespace, f"Expected whitespace tokens in output. Got: {tokens}"


def test_string_literals_are_identified_as_string_literal_tokens():
    """
    Scenario: String literals are identified as string literal tokens
    
    Given a source file containing a quoted string
    When I run the tokenizer with a lexer that defines a string_literal pattern
    Then the quoted string appears as a token with type "string_literal"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/string_test.py"
    with open(test_file, "w") as f:
        f.write('msg = "hello"\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    found_string = False
    for token in tokens:
        if token.get("value") == '"hello"' and token.get("type") == "string_literal":
            found_string = True
            break
    
    assert found_string, f"Expected string_literal token. Got: {tokens}"


def test_operators_are_identified_as_operator_tokens():
    """
    Scenario: Operators are identified as operator tokens
    
    Given a source file containing operators such as "+" or "="
    When I run the tokenizer with a lexer that defines operator tokens
    Then each operator appears as a token with type "operator"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/operator_test.py"
    with open(test_file, "w") as f:
        f.write('x = 1 + 2\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    found_equals = False
    found_plus = False
    for token in tokens:
        if token.get("value") == "=" and token.get("type") == "operator":
            found_equals = True
        if token.get("value") == "+" and token.get("type") == "operator":
            found_plus = True
    
    assert found_equals, f"Expected operator token for '='. Got: {tokens}"
    assert found_plus, f"Expected operator token for '+'. Got: {tokens}"


def test_keywords_are_not_misidentified_as_identifiers():
    """
    Scenario: Keywords are not misidentified as identifiers
    
    Given a source file where a keyword appears adjacent to an identifier
    When I run the tokenizer with the appropriate lexer
    Then the keyword token has type "keyword" not "identifier"
    And the identifier token has type "identifier"
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    test_file = "tests/fixtures/keyword_vs_identifier_test.py"
    with open(test_file, "w") as f:
        f.write('def my_func(): pass\n')  # 'def' is keyword, 'my_func' is identifier
    
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    def_token = None
    my_func_token = None
    for token in tokens:
        if token.get("value") == "def":
            def_token = token
        if token.get("value") == "my_func":
            my_func_token = token
    
    assert def_token is not None, f"Expected 'def' token. Got: {tokens}"
    assert my_func_token is not None, f"Expected 'my_func' token. Got: {tokens}"
    assert def_token.get("type") == "keyword", f"'def' should be keyword, got: {def_token}"
    assert my_func_token.get("type") == "identifier", f"'my_func' should be identifier, got: {my_func_token}"
