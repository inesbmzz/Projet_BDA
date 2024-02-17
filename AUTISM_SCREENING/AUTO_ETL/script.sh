#!/bin/bash

# Function to print separators
print_separator() {
    echo "=============================================================="
}

# Start of extraction
print_separator
echo "Starting extraction..."

# Run the extract.py script
python3 code/Extract.py

# Check if extract.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: extract.py failed"
    exit 1
fi

# Finish extraction
echo "Extraction finished successfully."

# Start of transformation
print_separator
echo "Starting transformation..."

# Run the transform.py script
python3 code/Transform.py

# Check if transform.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: transform.py failed"
    exit 1
fi

# Finish transformation
echo "Transformation finished successfully."

# Start of testing
print_separator
echo "Starting testing..."

# Run the test.py script
python3 code/Test.py

# Check if test.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: test.py failed"
    exit 1
fi

# Finish testing
echo "Testing finished successfully."

# End of script
print_separator
echo "Script execution completed."
