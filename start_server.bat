@echo off
chcp 65001 >nul
cls
echo ============================================================
echo WordPy CMS - WordPress com Python/Django
echo ============================================================
echo.
echo Verificando configuracao...
echo.

venv\Scripts\python test_server.py

echo.
echo ============================================================
echo Iniciando servidor de desenvolvimento...
echo ============================================================
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

venv\Scripts\python manage.py runserver

pause
