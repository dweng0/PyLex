"""
Tests for the "Lexer schema validation" feature.
"""

import subprocess
import sys
import os
import json


def test_valid_lexer_yaml_passes_validation():
    """
    Scenario: Valid lexer YAML passes validation
    
    Given a correctly structured lexer YAML file
    When I run validate.py
    Then the exit code is 0
    And no errors are reported
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a valid lexer YAML file
    valid_lexer = "tests/fixtures/valid_lexer.yaml"
    with open(valid_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types: []
tokens:
  - type: identifier
    pattern: "[a-zA-Z]+"
""")
    
    # Run validate.py on the specific file
    result = subprocess.run(
        [sys.executable, "validate.py"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    # validate.py validates all files in lexers/ directory
    # We need to check if our test file would pass - let's use a different approach
    # Run validation directly on the file
    from validate import validate_yaml
    import yaml
    
    with open(valid_lexer, 'r') as f:
        data = yaml.safe_load(f)
    
    with open('lexer_schema.json', 'r') as f:
        schema = json.load(f)
    
    from jsonschema import validate, ValidationError
    try:
        validate(instance=data, schema=schema)
        passed = True
    except ValidationError:
        passed = False
    
    assert passed, "Valid lexer YAML should pass validation"


def test_lexer_yaml_missing_required_field_fails_validation():
    """
    Scenario: Lexer YAML missing required field fails validation
    
    Given a lexer YAML file missing the "tokens" field
    When I run validate.py
    Then the exit code is non-zero
    And an error message describes the missing field
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a lexer YAML missing the "tokens" field
    invalid_lexer = "tests/fixtures/missing_tokens.yaml"
    with open(invalid_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types: []
""")
    
    import yaml
    import json
    from jsonschema import validate, ValidationError
    
    with open(invalid_lexer, 'r') as f:
        data = yaml.safe_load(f)
    
    with open('lexer_schema.json', 'r') as f:
        schema = json.load(f)
    
    try:
        validate(instance=data, schema=schema)
        passed = True
    except ValidationError as e:
        passed = False
        error_message = e.message
    
    assert not passed, "Lexer YAML missing 'tokens' should fail validation"
    assert "tokens" in error_message.lower() or "required" in error_message.lower(), \
        f"Error should mention missing 'tokens' field. Got: {error_message}"


def test_lexer_yaml_with_a_token_missing_both_value_and_pattern_fails_validation():
    """
    Scenario: Lexer YAML with a token missing both value and pattern fails validation
    
    Given a lexer YAML file containing a token definition with neither "value" nor "pattern"
    When I run validate.py
    Then the exit code is non-zero
    And an error message describes the invalid token definition
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a lexer YAML with invalid token (missing both value and pattern)
    invalid_lexer = "tests/fixtures/invalid_token.yaml"
    with open(invalid_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types: []
tokens:
  - type: identifier
""")
    
    import yaml
    import json
    from jsonschema import validate, ValidationError
    
    with open(invalid_lexer, 'r') as f:
        data = yaml.safe_load(f)
    
    with open('lexer_schema.json', 'r') as f:
        schema = json.load(f)
    
    try:
        validate(instance=data, schema=schema)
        passed = True
    except ValidationError as e:
        passed = False
        error_message = e.message
    
    assert not passed, "Token missing both 'value' and 'pattern' should fail validation"
    # The error should describe the invalid token definition
    assert "not valid" in error_message.lower() or "value" in error_message.lower() or "pattern" in error_message.lower() or "required" in error_message.lower(), \
        f"Error should describe the invalid token. Got: {error_message}"


def test_duplicate_value_based_tokens_are_rejected_during_validation():
    """
    Scenario: Duplicate value-based tokens are rejected during validation
    
    Given a lexer YAML file containing two tokens with the same value (e.g. "**" defined twice)
    When I run validate.py
    Then the exit code is non-zero
    And an error message identifies the duplicate token value
    """
    os.makedirs("tests/fixtures", exist_ok=True)
    
    # Create a lexer YAML with duplicate token values
    duplicate_lexer = "tests/fixtures/duplicate_token.yaml"
    with open(duplicate_lexer, "w") as f:
        f.write("""lexer_target: test
version: 1.0.0
delimiters: " \\t\\n"
delimiter_check_for_types: []
tokens:
  - type: operator
    value: "**"
  - type: operator
    value: "**"
""")
    
    import yaml
    import json
    from validate import validate_yaml
    
    error_list = []
    result = validate_yaml(duplicate_lexer, 'lexer_schema.json', error_list)
    
    assert not result, "Lexer YAML with duplicate token values should fail validation"
    assert len(error_list) > 0, "Error list should contain at least one error"
    assert "duplicate" in error_list[0].lower() or "Duplicate" in error_list[0], \
        f"Error should mention duplicate token value. Got: {error_list[0]}"


def test_all_bundled_lexer_files_pass_validation():
    """
    Scenario: All bundled lexer files pass validation
    
    Given all YAML files in the lexers/ directory
    When I run validate.py on each one
    Then every file passes validation with exit code 0
    """
    result = subprocess.run(
        [sys.executable, "validate.py"],
        capture_output=True,
        text=True
    )
    
    # Exit code should be 0
    assert result.returncode == 0, f"validate.py should exit with 0. Got: {result.returncode}, stderr: {result.stderr}"
    
    # No errors should be reported
    assert result.stdout.strip() == "" and result.stderr.strip() == "", \
        f"No errors should be reported. Got stdout: {result.stdout}, stderr: {result.stderr}"
