# Journal

<!-- Agent writes entries here, newest at the top. Never delete entries. -->
<!-- Format: ## Day N — HH:MM — [short title] -->

## 2026-03-18 08:14 — Complete BDD coverage (4 scenarios)

Covered all 4 remaining uncovered scenarios: added exception handling in main.py for FileNotFoundError, PermissionError, and yaml.YAMLError to eliminate tracebacks from CLI error messages. Refactored get_string_slice() in lexers/lexer.py to use direct string slicing instead of character-by-character concatenation. All 49/49 scenarios now covered and passing. Project is complete.

## 2026-03-18 07:52 — BDD coverage improvements (6 scenarios)

Fixed the check_bdd_coverage.py script to handle special characters like "++" and "-" in scenario names. Added test for "Duplicate value-based tokens are rejected during validation" scenario and implemented duplicate token detection in validate.py. Fixed duplicate token values in bundled lexer files (python.yaml, vyper.yaml, rust.yaml, javascript.yaml). Implemented regex pattern precompilation feature with precompile_patterns() function in lexer.py and added two tests. Now at 45/49 scenarios covered. Remaining: string slice extraction test and three CLI error message tests (no traceback). Next session should tackle the CLI error message scenarios to eliminate Python tracebacks from stderr.
