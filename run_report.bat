@echo off
set PROJECT_DIR=C:\Users\felip\Desktop\hotel_automation
cd /d %PROJECT_DIR%

call .venv\Scripts\activate

python -m src.main

REM opcional: para que el scheduler capture un errorlevel
exit /b %errorlevel% 