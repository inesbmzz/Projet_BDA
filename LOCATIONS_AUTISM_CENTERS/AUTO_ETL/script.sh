#!/bin/bash

# Create the log directory
mkdir -p log

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt 1> log/install.log 2> log/install.error

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Error: Installation failed"
    exit 1
fi

# Start of extraction
echo "Starting extraction..."

# Run the extract.py script
python3 code/Extract.py 1> log/extract.log 2> log/extract.error

# Check if extract.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: extract.py failed"
    exit 1
fi

# Finish extraction
echo "Extraction finished successfully."

# Start of transformation
echo "Starting transformation..."

# Run the transform.py script
python3 code/Transform.py 1> log/transform.log 2> log/transform.error

# Check if transform.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: transform.py failed"
    exit 1
fi

# Finish transformation
echo "Transformation finished successfully."

# Start of testing
echo "Starting testing..."

# Run the test.py script
python3 code/Test.py 2> log/test.error

# Check if test.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: test.py failed"
    exit 1
fi

# Finish testing
echo "Testing finished successfully."

# Run Load.py 1 script
echo "Creating database tables..."
python3 code/Load.py 1 1> log/load.log 2> log/load.error

# Check if Load.py 1 ran successfully
if [ $? -ne 0 ]; then
    echo "Error: Load.py 1 failed"
    exit 1
fi

# Finish Load.py 1
echo "Database tables created successfully."

# Start SQL Loader
echo "Starting SQL Loader..."

# Run the SQL Loader script
sqlldr SID/Oracle21c@orcl control=code/autism_centers_loader.ctl log=log\sqlldr.log bad=log\sqlldr.bad

# Finish SQL Loader
echo "SQL Loader finished successfully."

# Start of Load.py 2
echo "Loading data into database..."
python3 code/Load.py 2 1> log/load.log 2> log/load.error

# Check if Load.py 2 ran successfully
if [ $? -ne 0 ]; then
    echo "Error: Load.py 2 failed"
    exit 1
fi

# Finish Load.py 2
echo "Data loaded successfully."

# End of script
echo "Script execution completed."
