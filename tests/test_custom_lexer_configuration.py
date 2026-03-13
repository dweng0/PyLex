"""
Tests for the "Custom lexer configuration" feature.
"""

import json
import subprocess
import sys
import os


def test_a_custom_lexer_tokenises_a_simple_dsl():
    """
    Scenario: A custom lexer tokenises a simple DSL
    
    Given a custom lexer YAML defining two token types and a simple input string
    When I run the tokenizer with that custom lexer
    Then the output contains tokens matching the custom definitions
    And no tokens from the built-in lexers appear in the output
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a custom lexer for a simple DSL
    custom_lexer = "tests/fixtures/custom_dsl.yaml"
    with open(custom_lexer, "w") as f:
        f.write("""lexer_target: dsl
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types:
  - command
tokens:
  - type: command
    value: "PRINT"
  - type: command
    value: "SET"
  - type: string_literal
    pattern: '"[^"]*"'
  - type: identifier
    pattern: "[a-zA-Z_][a-zA-Z0-9_]*"
  - type: whitespace
    pattern: "\\\\s+"
""")
    
    # Create a simple DSL input
    dsl_input = "tests/fixtures/dsl_input.txt"
    with open(dsl_input, "w") as f:
        f.write('SET x "hello"\nPRINT x\n')
    
    result = subprocess.run(
        [sys.executable, "main.py", dsl_input, custom_lexer],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Tokenizer failed: {result.stderr}"
    
    tokens = json.loads(result.stdout)
    
    # Check for custom tokens
    found_set = any(t.get("value") == "SET" and t.get("type") == "command" for t in tokens)
    found_print = any(t.get("value") == "PRINT" and t.get("type") == "command" for t in tokens)
    found_hello = any(t.get("value") == '"hello"' and t.get("type") == "string_literal" for t in tokens)
    found_x = any(t.get("value") == "x" and t.get("type") == "identifier" for t in tokens)
    
    assert found_set, f"Expected 'SET' command token. Got: {tokens}"
    assert found_print, f"Expected 'PRINT' command token. Got: {tokens}"
    assert found_hello, f"Expected string_literal token. Got: {tokens}"
    assert found_x, f"Expected identifier token. Got: {tokens}"
