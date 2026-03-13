#!/bin/bash
set -e

pip install -r requirements.txt --quiet
python3 -m py_compile main.py tokenizer/tokenizer.py lexers/lexer.py validate.py hard_validate.py

echo "Build complete."
