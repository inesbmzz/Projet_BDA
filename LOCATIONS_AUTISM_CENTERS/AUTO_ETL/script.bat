@echo off

rem Create log directory
mkdir log

rem Install the required packages
echo Installing required packages...
pip install -r requirements.txt 1> log\install.log 2> log\install.err

rem Check if installation was successful
if not %errorlevel% == 0 (
    echo Error: Failed to install required packages
    exit /b 1
)

rem Start of extraction
echo Starting extraction...

rem Run the extract.py script
python code\Extract.py 1> log\extract.log 2> log\extract.err

rem Check if extract.py ran successfully
if not %errorlevel% == 0 (
    echo Error: extract.py failed
    exit /b 1
)

rem Finish extraction
echo Extraction finished successfully.

rem Start of transformation
echo Starting transformation...

rem Run the transform.py script
python code\Transform.py 1> log\transform.log 2> log\transform.err

rem Check if transform.py ran successfully
if not %errorlevel% == 0 (
    echo Error: transform.py failed
    exit /b 1
)

rem Finish transformation
echo Transformation finished successfully.

rem Start of testing
echo Starting testing...

rem Run the test.py script
python code\Test.py 2> log\test.err

rem Check if test.py ran successfully
if not %errorlevel% == 0 (
    echo Error: test.py failed
    exit /b 1
)

rem Finish testing
echo Testing finished successfully.

rem Run Load.py 1
echo Creating database tables...
python code\Load.py 1 1> log\load.log 2> log\load.err

rem Check if Load.py ran successfully
if not %errorlevel% == 0 (
    echo Error: Load.py 1 failed

)

rem Finish Load 1
echo Database tables creation finished successfully.

rem Start SQL Loader
echo Starting SQL Loader...

rem Run sqlldr command
sqlldr SID/Oracle21c@orcl control=code/autism_centers_loader.ctl log=log\sqlldr.log bad=log\sqlldr.bad

rem Finish SQL Loader
echo SQL Loader finished successfully.

rem Run Load.py 2
echo Loading data into database...
python code\Load.py 2 1> log\load.log 2> log\load.err

rem Check if Load.py ran successfully
if not %errorlevel% == 0 (
    echo Error: Load.py 2 failed
    exit /b 1
)

rem Finish Load 2
echo Data loading finished successfully.

rem End of script
echo Script execution completed.