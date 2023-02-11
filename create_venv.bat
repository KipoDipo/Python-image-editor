@echo off
echo Setting up Virtual Environment...
py -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
pause