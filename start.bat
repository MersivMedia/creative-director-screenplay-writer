@echo off
SETLOCAL EnableDelayedExpansion

REM Function to check if setup is needed
SET SETUP_NEEDED=0

REM Check if virtual environment exists
IF NOT EXIST "venv" SET SETUP_NEEDED=1

REM Check if requirements are installed
IF EXIST "venv" (
    call venv\Scripts\activate.bat
    IF !ERRORLEVEL! NEQ 0 (
        echo Error activating virtual environment
        SET SETUP_NEEDED=1
    ) ELSE (
        pip freeze > temp_installed.txt
        FOR /F "tokens=*" %%A IN (requirements.txt) DO (
            findstr /I /C:"%%A" temp_installed.txt > nul
            IF !ERRORLEVEL! NEQ 0 SET SETUP_NEEDED=1
        )
        del temp_installed.txt
        call venv\Scripts\deactivate.bat
    )
)

REM Run setup if needed
IF !SETUP_NEEDED!==1 (
    echo Initial setup needed. Running setup script...
    call setup.bat
    IF !ERRORLEVEL! NEQ 0 (
        echo Error: Setup failed. Please check the error messages above.
        exit /b 1
    )
)

REM Activate virtual environment and start the application
echo Starting Screenwriter application...
call venv\Scripts\activate.bat
IF !ERRORLEVEL! NEQ 0 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

REM Verify streamlit is installed
where streamlit >nul 2>nul
IF !ERRORLEVEL! NEQ 0 (
    echo Error: Streamlit not found. Trying to install it...
    pip install streamlit
    IF !ERRORLEVEL! NEQ 0 (
        echo Error: Failed to install streamlit
        exit /b 1
    )
)

echo Starting Streamlit server...
python -m streamlit run main.py
IF !ERRORLEVEL! NEQ 0 (
    echo Error: Failed to start Streamlit server
    exit /b 1
)

exit /b 0 