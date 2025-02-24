@echo off

echo Activating the virtual environment...
call .\.venv\Scripts\activate

echo Compiling...
pyinstaller --onefile --console --icon=assets/icon.ico vk_downloader.py

echo Compilation completed!
pause
