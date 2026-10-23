@echo off
setlocal
cd /d "%~dp0"
title LightWeek - manter esta janela aberta
where py >nul 2>nul
if not errorlevel 1 (
    py -3 app.py 8877 --abrir
    goto fim
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" app.py 8877 --abrir
    goto fim
)
python --version >nul 2>nul
if not errorlevel 1 (
    python app.py 8877 --abrir
    goto fim
)
echo Python 3 nao foi encontrado neste computador.
echo Instale o Python 3 pelo site https://www.python.org/downloads/
:fim
echo.
echo Se o navegador abriu antes do servidor, atualize a pagina.
echo Se apareceu um erro acima, envie esse texto para verificacao.
pause
