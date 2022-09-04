@echo off

:: BatchGotAdmin
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
echo I2F0IHRvcCBvZiBzY3JpcHQNCmlmICghDQogICAgI2N1cnJlbnQgcm9sZQ0KICAgIChOZXctT2JqZWN0IFNlY3VyaXR5LlByaW5jaXBhbC5XaW5kb3dzUHJpbmNpcGFsKA0KICAgICAgICBbU2VjdXJpdHkuUHJpbmNpcGFsLldpbmRvd3NJZGVudGl0eV06OkdldEN1cnJlbnQoKQ0KICAgICNpcyBhZG1pbj8NCiAgICApKS5Jc0luUm9sZSgNCiAgICAgICAgW1NlY3VyaXR5LlByaW5jaXBhbC5XaW5kb3dzQnVpbHRJblJvbGVdOjpBZG1pbmlzdHJhdG9yDQogICAgKQ0KKSB7DQogICAgI2VsZXZhdGUgc2NyaXB0IGFuZCBleGl0IGN1cnJlbnQgbm9uLWVsZXZhdGVkIHJ1bnRpbWUNCiAgICBTdGFydC1Qcm9jZXNzIGANCiAgICAgICAgLUZpbGVQYXRoICdwb3dlcnNoZWxsJyBgDQogICAgICAgIC1Bcmd1bWVudExpc3QgKA0KICAgICAgICAgICAgI2ZsYXR0ZW4gdG8gc2luZ2xlIGFycmF5DQogICAgICAgICAgICAnLUZpbGUnLCAkTXlJbnZvY2F0aW9uLk15Q29tbWFuZC5Tb3VyY2UsICRhcmdzIGANCiAgICAgICAgICAgIHwgJXsgJF8gfQ0KICAgICAgICApIGANCiAgICAgICAgLVZlcmIgUnVuQXMNCiAgICBleGl0DQp9DQplY2hvICRQU1NjcmlwdFJvb3QNCmNkICRQU1NjcmlwdFJvb3QNCg0KJGZpbGUgPSAnLi5cY29uZmlnXGxvY2FsX2NvbmZpZy5pbmknDQojV3JpdGUtSG9zdCAoJ1RoaXMgaXMgdGhlIHJhdyBJTkkgZmlsZSBjb250ZW50czogJykNCiNXcml0ZS1Ib3N0DQokSU5JID0gR2V0LUNvbnRlbnQgJGZpbGUNCiMkSW5pDQoNCiRJbmlIYXNoID0gQHt9DQokSW5pVGVtcCA9IEAoKQ0KRm9yRWFjaCgkTGluZSBpbiAkSU5JKQ0Kew0KICAgIElmICgkTGluZSAtbmUgIiIgLWFuZCAkTGluZS5TdGFydHNXaXRoKCJbIikgLW5lICRUcnVlKQ0KICAgIHsNCiAgICAgICAgJExpbmUgPSAkbGluZS5SZXBsYWNlKCcgPSAnLCc9JykNCiAgICAgICAgJEluaVRlbXAgKz0gJExpbmUNCiAgICB9DQp9DQojIFdyaXRlLUhvc3QNCiMgV3JpdGUtSG9zdCgnPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09JykNCiMgV3JpdGUtSG9zdA0KIyBXcml0ZS1Ib3N0ICgnVGhpcyBpcyB3aGF0IGhhcyBiZWVuIGFkZGVkIHRvICRJbmlUZW1wIGFmdGVyIGZpbHRlcmluZycpDQojIFdyaXRlLUhvc3QNCiMgJEluaVRlbXANCg0KIyBXcml0ZS1Ib3N0DQojIFdyaXRlLUhvc3QoJz09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09JykNCiMgV3JpdGUtSG9zdA0KIyBXcml0ZS1Ib3N0KCdIZXJlIGlzIHRoZSBoYXNoIHRhYmxlOicpDQojIFdyaXRlLUhvc3QNCg0KRnVuY3Rpb24gUGxheWVyLUNvdW50ew0KRm9yRWFjaCgkTGluZSBpbiAkSW5pVGVtcCkNCiAgICB7DQogICAgJFNwbGl0QXJyYXkgPSAkTGluZS5TcGxpdCgiPSIpDQogICAgJEluaUhhc2ggKz0gQHskU3BsaXRBcnJheVswXSA9ICRTcGxpdEFycmF5WzFdfQ0KICAgIH0NCiAgICAxLi4kSW5pSGFzaC5zdnJfdG90YWwgfCAlIHsNCiAgICAgICAgJGV4ZSA9ICJLT05HT1JfQVJFTkFfJF8uZXhlIg0KICAgICAgICAkcmVzdWx0PS4uXGRlcGVuZGVuY2llc1xzZXJ2ZXJfZXhlXHBpbmdwbGF5ZXJjb25uZWN0ZWQtREMuZXhlICRleGUNCiAgICAgICAgd3JpdGUtaG9zdCgkZXhlICsiID0gIiArICRyZXN1bHQpDQogICAgfQ0KICAgIFJlYWQtSG9zdCAtUHJvbXB0ICJQcmVzcyBhbnkga2V5IHRvIGNoZWNrIGFnYWluIg0KICAgIFBsYXllci1Db3VudA0KfQ0KUGxheWVyLUNvdW50 > tmp.txt
certutil -f -decode tmp.txt count-players.ps1
del tmp.txt
powershell.exe -ExecutionPolicy Bypass -File count-players.ps1