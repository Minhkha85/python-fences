@echo off
cd /d "%~dp0"

:: Check for admin rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Check if Python and required files exist
if not exist "venv\Scripts\pythonw.exe" (
    echo Error: pythonw.exe not found in venv\Scripts
    echo Please ensure you have set up the virtual environment correctly
    pause
    exit /B
)

if not exist "main.py" (
    echo Error: main.py not found
    echo Please ensure you are running this script from the correct directory
    pause
    exit /B
)

:: Install required packages if needed
echo Installing required packages...
venv\Scripts\pip.exe install -r requirements.txt

:: Run the Python script with pythonw.exe
echo Starting application...
start "" /wait "venv\Scripts\pythonw.exe" "main.py"

:: Check if application started successfully
if %errorlevel% NEQ 0 (
    echo Error: Application failed to start
    echo Check debug.log for more information
    pause
) else (
    echo Application started successfully
)

pause 