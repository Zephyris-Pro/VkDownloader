@echo off

IF NOT EXIST ".venv" (
    echo Creating the virtual environment...
    py -m venv .venv
)

echo Activating the virtual environment...
call .\.venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Installation completed!
pause
