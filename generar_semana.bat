@echo off
chcp 65001 > nul
echo ============================================================
echo 📦 GENERANDO PACK SEMANAL DE VÍDEOS Y TEXTOS RADARALERTAS
echo ============================================================
cd /d "%~dp0"
call .venv\Scripts\activate
python src\video_generator\generar_pack_semanal.py
echo.
echo Abriendo carpeta con los vídeos de la semana...
start explorer "%~dp0output\semana_actual"
pause
