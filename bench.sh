#!/bin/bash

DEFAULT_FILE="rtow/__main__.py"

if [ $# -eq 0 ]; then
    FILE_PATH=$DEFAULT_FILE
else
    FILE_PATH="$1"
fi

codon build -exe "$FILE_PATH"

EXECUTABLE_NAME=$(dirname "$FILE_PATH")/$(basename -s .py "$FILE_PATH")
MODULE_NAME=${FILE_PATH//\//.}
MODULE_NAME=${MODULE_NAME%.py}

echo "CODON:"
time "$EXECUTABLE_NAME"

echo "PYTHON:"
time python -m "$MODULE_NAME"

rm "$EXECUTABLE_NAME"
rm -rf "${EXECUTABLE_NAME}.dSYM"
