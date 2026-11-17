@echo off
cd /d "C:\Ideas\radar-alertas"
call .\.venv\Scripts\activate.bat
python src\orquestador_diario.py >> logs_diario.txt 2>&1
