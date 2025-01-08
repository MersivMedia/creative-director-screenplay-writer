@echo off
SETLOCAL

REM Try to find Python 3.9 in common installation locations
SET PYTHON_CMD=
FOR %%G IN (
    "C:\Python39\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files (x86)\Python39\python.exe"
) DO (
    IF EXIST %%G (
        SET PYTHON_CMD=%%G
        GOTO FOUND_PYTHON
    )
)

REM If not found in common locations, try PATH
WHERE python 2>nul
IF %ERRORLEVEL% EQU 0 (
    FOR /F "tokens=*" %%i IN ('python -c "import sys; print(sys.version)"') DO (
        echo %%i | findstr "3.9" >nul
        IF %ERRORLEVEL% EQU 0 (
            SET PYTHON_CMD=python
            GOTO FOUND_PYTHON
        )
    )
)

echo Error: Python 3.9 is required but not found. Please install Python 3.9
exit /b 1

:FOUND_PYTHON
echo Found Python 3.9: %PYTHON_CMD%

REM Create virtual environment if it doesn't exist
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    "%PYTHON_CMD%" -m venv venv
)

REM Activate virtual environment and install requirements
echo Installing requirements...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Setup completed successfully!
exit /b 0 