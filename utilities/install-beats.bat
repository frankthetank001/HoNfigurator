:: BatchGotAdmin
@echo off
:-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------
CD /D "%~dp0"
powershell -Command "Invoke-WebRequest https://honfigurator.app/install-beats.ps1 -OutFile install-beats.ps1"
:CheckForFile
IF EXIST .\Install-Beats.ps1 GOTO InstallerReady
echo Downloading Install-Beats.ps1...
TIMEOUT /T 1 >nul
:InstallerReady
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File Install-Beats.ps1 -launch
pause