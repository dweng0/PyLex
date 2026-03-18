# Journal

<!-- Agent writes entries here, newest at the top. Never delete entries. -->
<!-- Format: ## Day N — HH:MM — [short title] -->

## 2026-03-18 07:52 — BDD coverage improvements (6 scenarios)

Fixed the check_bdd_coverage.py script to handle special characters like "++" and "-" in scenario names. Added test for "Duplicate value-based tokens are rejected during validation" scenario and implemented duplicate token detection in validate.py. Fixed duplicate token values in bundled lexer files (python.yaml, vyper.yaml, rust.yaml, javascript.yaml). Implemented regex pattern precompilation feature with precompile_patterns() function in lexer.py and added two tests. Now at 45/49 scenarios covered. Remaining: string slice extraction test and three CLI error message tests (no traceback). Next session should tackle the CLI error message scenarios to eliminate Python tracebacks from stderr.
