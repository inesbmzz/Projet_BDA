#!/bin/bash

echo "Install python packages..."
python3 -m pip install pandas beautifulsoup4 PyMuPDF

clear
# Function to print separators
print_separator() {
    echo "=============================================================="
}

# Start of extraction
print_separator
echo "Starting extraction..."

python3 code/extract/child_mind.py

if [ $? -ne 0 ]; then
    echo "Error: child_mind.py failed"
    exit 1
fi


mkdir -p data/extract_out/medscape/answer
mkdir -p data/extract_out/medscape/question

python3 code/extract/medscape.py

if [ $? -ne 0 ]; then
    echo "Error: medscape.py failed"
    exit 1
fi

python3 code/extract/parent_guide.py

if [ $? -ne 0 ]; then
    echo "Error: parent_guide.py failed"
    exit 1
fi

# Finish extraction
echo "Extraction finished successfully."


# Delay for 10 seconds
echo "ines rah tmodifi..."
sleep 10


# Start of transformation
print_separator
echo "Starting transformation..."

# Run the transform.py script
python3 code/transform/process_data.py

# Check if transform.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: transform.py failed"
    exit 1
fi

# Finish transformation
echo "Transformation finished successfully."


# Start of transformation
print_separator
echo "Starting testing..."

# Run the transform.py script
python3 code/test/test.py

# Check if transform.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: test.py failed"
    exit 1
fi

# Finish transformation
echo "testing finished successfully."

