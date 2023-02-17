#!/bin/bash

cd ../backend

# Run black to format code
echo && echo "Running black..."
poetry run black .

# Run pylint to check for errors and warnings
echo && echo "Running pylint..."
poetry run pylint . --max-line-length 120

# Run pyupgrade to update Python code to a newer version
echo && echo "Running pyupgrade..."
poetry run pyupgrade

# Run docformatter to format docstrings in-place
echo && echo "Running docformatter..."
poetry run docformatter -c -r .
# Run mypy to check for type annotations
echo && echo "Running mypy..."
poetry run mypy .
#
## Run autoflake to remove unused variables and imports
echo && echo "Running autoflake..."
poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports .

echo "Refactoring complete!"