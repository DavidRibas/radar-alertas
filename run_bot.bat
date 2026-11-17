@echo off
title RadarAlertas - Bot Telegram Interactivo
cd /d "%~dp0"
echo ========================================================
echo   Iniciando Bot Interactivo de Telegram RadarAlertas
echo ========================================================
.\.venv\Scripts\python.exe -m src.telegram_bot.bot_alertas
pause
