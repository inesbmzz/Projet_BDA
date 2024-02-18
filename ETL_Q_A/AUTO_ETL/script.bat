@echo off
:: Start of extraction
echo "Install python packages..."
python -m pip install pandas beautifulsoup4 PyMuPDF

clear

:: Start of extraction
echo "Starting extraction..."

python code\extract\child_mind.py

if not %errorlevel% == 0 (
    echo "Error: child_mind.py failed"
    exit /b 1
)

mkdir data\extract_out\medscape\answer
mkdir data\extract_out\medscape\question

python code\extract\medscape.py

if not %errorlevel% == 0 (
    echo "Error: medscape.py failed"
    exit /b 1
)

python code\extract\parent_guide.py

if not %errorlevel% == 0 (
    echo "Error: parent_guide.py failed"
    exit /b 1
)

:: Finish extraction
echo "Extraction finished successfully."

:: Delay for 10 seconds
echo "ines rah tmodifi..."
timeout /t 10

:: Start of transformation
echo "Starting transformation..."

:: Run the process_data.py script
python code\transform\process_data.py

:: Check if process_data.py ran successfully
if not %errorlevel% == 0 (
    echo "Error: process_data.py failed"
    exit /b 1
)

:: Finish transformation
echo "Transformation finished successfully."

:: Start of testing
echo "Starting testing..."

:: Run the test.py script
python code\test\test.py

:: Check if test.py ran successfully
if not %errorlevel% == 0 (
    echo "Error: test.py failed"
    exit /b 1
)

:: Finish testing
echo "Testing finished successfully."

:: Start of loading
echo "Starting loading..."

:: Run node loading script
cd code\load

:: Install node packages
echo "Install node packages..."
npm install

:: Start the loading
echo "Loading data..."
npm start

:: Check if loading ran successfully
if not %errorlevel% == 0 (
    echo "Error: Loading failed"
    exit /b 1
)

:: Finish loading
echo "Loading finished successfully."

:: Testing loading
echo "Testing loading..."
npm test

:: Check if loading test ran successfully
if not %errorlevel% == 0 (
    echo "Error: Loading test failed"
    exit /b 1
)

:: Finish loading test
echo "Loading test finished successfully."

:: Finish ETL
echo "Script execution completed."

:: Exit with no error
exit /b
