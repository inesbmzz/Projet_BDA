@echo off

rem Install requests and pandas
echo Installing requests and pandas...
pip install requests pandas cx_Oracle

rem Check if installation was successful
if not %errorlevel% == 0 (
    echo Error: Failed to install requests or pandas or cx_Oracle
    exit /b 1
)

rem Check if installation was successful
if not %errorlevel% == 0 (
    echo Error: cx_Oracle installation failed
    exit /b 1
)

rem Start of extraction
echo Starting extraction...

rem Run the extract.py script
python code\Extract.py

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
python code\Transform.py

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
python code\Test.py

rem Check if test.py ran successfully
if not %errorlevel% == 0 (
    echo Error: test.py failed
    exit /b 1
)

rem Finish testing
echo Testing finished successfully.



rem Run Load.py
echo Running Load.py...
python code\Load.py

rem Check if Load.py ran successfully
if not %errorlevel% == 0 (
    echo Error: Load.py failed

)


rem Finish Load
echo Load finished successfully.

rem Start SQL Loader
echo Starting SQL Loader...

rem Run sqlldr command
sqlldr SID/Oracle21c@orcl control=code/autism_screening_loader.ctl

rem Finish SQL Loader
echo SQL Loader finished successfully.

rem End of script
echo Script execution completed.


:wait
timeout /t 100 /nobreak