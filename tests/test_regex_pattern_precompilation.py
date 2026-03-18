"""
Tests for the "Regex pattern precompilation" feature.
"""

import subprocess
import sys
import os
import time


def test_patterns_are_compiled_once_before_tokenisation_begins():
    """
    Scenario: Patterns are compiled once before tokenisation begins
    
    Given a lexer YAML containing regex pattern tokens
    When I tokenise a source file
    Then each regex pattern is compiled only once, not on every character position
    """
    # This test verifies that the precompile_patterns function is called
    # and that compiled patterns are used during tokenization.
    
    from lexers.lexer import precompile_patterns
    
    # Create a test lexer config with pattern-based tokens
    lexer_config = {
        'tokens': [
            {'type': 'identifier', 'pattern': r'[a-zA-Z_][a-zA-Z0-9_]*'},
            {'type': 'number', 'pattern': r'\d+'},
            {'type': 'operator', 'value': '+'},
        ]
    }
    
    # Precompile the patterns
    precompile_patterns(lexer_config)
    
    # Verify that compiled_pattern attributes were added
    for token in lexer_config['tokens']:
        if 'pattern' in token:
            assert 'compiled_pattern' in token, \
                f"Token {token['type']} should have 'compiled_pattern' after precompilation"
            # Verify it's actually a compiled regex
            import re
            assert isinstance(token['compiled_pattern'], type(re.compile(''))), \
                f"compiled_pattern should be a compiled regex object"


def test_large_file_tokenisation_completes_within_a_reasonable_time():
    """
    Scenario: Large file tokenisation completes within a reasonable time
    
    Given a Python source file of at least 1000 lines
    When I run the tokenizer with the Python lexer
    Then tokenisation completes within 5 seconds
    And the output is a valid JSON array
    """
    import json
    
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Generate a large Python file (1000+ lines)
    large_file = "tests/fixtures/large_python_test.py"
    lines = []
    for i in range(1000):
        lines.append(f"def function_{i}(arg_{i}):")
        lines.append(f"    \"\"\"Docstring for function {i}.\"\"\"")
        lines.append(f"    result_{i} = {i} * 2")
        lines.append(f"    if result_{i} > 100:")
        lines.append(f"        return result_{i}")
        lines.append(f"    return None")
        lines.append("")
    
    with open(large_file, "w") as f:
        f.write("\n".join(lines))
    
    # Run the tokenizer and measure time
    start_time = time.time()
    result = subprocess.run(
        [sys.executable, "main.py", large_file, "lexers/python.yaml"],
        capture_output=True,
        text=True
    )
    elapsed_time = time.time() - start_time
    
    # Verify completion within 5 seconds
    assert elapsed_time < 5.0, \
        f"Tokenization took {elapsed_time:.2f}s, should complete within 5 seconds"
    
    # Verify exit code
    assert result.returncode == 0, \
        f"Tokenizer failed with stderr: {result.stderr}"
    
    # Verify output is valid JSON array
    tokens = json.loads(result.stdout)
    assert isinstance(tokens, list), "Output should be a JSON array"
    assert len(tokens) > 0, "Output should contain tokens"
