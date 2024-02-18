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

# Start of loading
print_separator
echo "Starting loading..."

# Run the load.py script
cd code/load

# Install node modules
echo "Installing node modules..."
npm install

# Start the loading
echo "Loading data..."
npm start

# Check if loading ran successfully
if [ $? -ne 0 ]; then
    echo "Error: load.py failed"
    exit 1
fi

# Finish loading
echo "Loading finished successfully."

# Testing loading
print_separator
echo "Starting testing loading..."
npm test

# Check if loading ran successfully
if [ $? -ne 0 ]; then
    echo "Error: load.py failed"
    exit 1
fi

# Finish loading
echo "Loading finished successfully."

# End of ETL
print_separator
echo "Script execution completed."

# Exit with no error
exit 0