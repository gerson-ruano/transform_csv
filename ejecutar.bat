@echo off
title Procesador de CSV a Excel
cls

echo ===============================
echo     PROCESADOR CSV TO EXCEL
echo ===============================

cd /d "%~dp0"

echo Procesando, por favor espere...

echo.
dist\ProcesadorCSV.exe

echo.
echo ===============================
echo [OK] Procesamiento completado!
echo ===============================
echo.
pause


