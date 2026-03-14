"""
Tests for the "Import statement tokenisation" feature.
"""

import json
import subprocess
import sys
import os


def test_rust_use_statement_is_tokenised_correctly():
    """
    Scenario: Rust use statement is tokenised correctly
    
    Given a Rust source file containing a use statement
    When I run the tokenizer with the Rust lexer
    Then "use" appears as a keyword token
    And the imported module/path appears as an identifier token
    """
    # Create a test file with a Rust use statement
    test_file = "tests/fixtures/rust_use_statement.rs"
    os.makedirs("tests/fixtures", exist_ok=True)
    
    with open(test_file, "w") as f:
        f.write('use std::io;\n\nfn main() {\n    println!("Hello");\n}\n')
    
    # Run the tokenizer with Rust lexer
    result = subprocess.run(
        [sys.executable, "main.py", test_file, "lexers/rust.yaml"],
        capture_output=True,
        text=True
    )
    
    # Check exit code
    assert result.returncode == 0, f"Tokenizer failed with stderr: {result.stderr}"
    
    # Parse the output as JSON
    tokens = json.loads(result.stdout)
    
    # Verify it's a list (JSON array)
    assert isinstance(tokens, list), "Output should be a JSON array"
    
    # Verify "use" appears as a keyword token
    found_use_keyword = False
    for token in tokens:
        if token.get("value") == "use" and token.get("type") == "keyword":
            found_use_keyword = True
            break
    
    assert found_use_keyword, f"Expected a keyword token for 'use' in output. Got: {tokens}"
    
    # Verify "std" and "io" appear as identifier tokens
    found_std = False
    found_io = False
    for token in tokens:
        if token.get("value") == "std" and token.get("type") == "identifier":
            found_std = True
        if token.get("value") == "io" and token.get("type") == "identifier":
            found_io = True
    
    assert found_std, f"Expected an identifier token for 'std' in output. Got: {tokens}"
    assert found_io, f"Expected an identifier token for 'io' in output. Got: {tokens}"
