@rem Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
@rem Student No(s)#: 231805033, 231805026
@rem General Comments: Windows command wrapper for tools/set-author.ps1.
@echo off
setlocal
where pwsh >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0set-author.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0set-author.ps1" %*
)
exit /b %ERRORLEVEL%
