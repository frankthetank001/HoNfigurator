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
echo I2F0IHRvcCBvZiBzY3JpcHQNCmlmICghDQogICAgI2N1cnJlbnQgcm9sZQ0KICAgIChOZXctT2JqZWN0IFNlY3VyaXR5LlByaW5jaXBhbC5XaW5kb3dzUHJpbmNpcGFsKA0KICAgICAgICBbU2VjdXJpdHkuUHJpbmNpcGFsLldpbmRvd3NJZGVudGl0eV06OkdldEN1cnJlbnQoKQ0KICAgICNpcyBhZG1pbj8NCiAgICApKS5Jc0luUm9sZSgNCiAgICAgICAgW1NlY3VyaXR5LlByaW5jaXBhbC5XaW5kb3dzQnVpbHRJblJvbGVdOjpBZG1pbmlzdHJhdG9yDQogICAgKQ0KKSB7DQogICAgI2VsZXZhdGUgc2NyaXB0IGFuZCBleGl0IGN1cnJlbnQgbm9uLWVsZXZhdGVkIHJ1bnRpbWUNCiAgICBTdGFydC1Qcm9jZXNzIGANCiAgICAgICAgLUZpbGVQYXRoICdwb3dlcnNoZWxsJyBgDQogICAgICAgIC1Bcmd1bWVudExpc3QgKA0KICAgICAgICAgICAgI2ZsYXR0ZW4gdG8gc2luZ2xlIGFycmF5DQogICAgICAgICAgICAnLUZpbGUnLCAkTXlJbnZvY2F0aW9uLk15Q29tbWFuZC5Tb3VyY2UsICRhcmdzIGANCiAgICAgICAgICAgIHwgJXsgJF8gfQ0KICAgICAgICApIGANCiAgICAgICAgLVZlcmIgUnVuQXMNCiAgICBleGl0DQp9DQpmdW5jdGlvbiBJbnNlcnQtQ29udGVudCAoJGZpbGUpIHsNCiAgICBCRUdJTiB7DQogICAgJGNvbnRlbnQgPSBHZXQtQ29udGVudCAkZmlsZQ0KICAgIH0NCiAgICBQUk9DRVNTIHsNCiAgICAkXyB8IFNldC1Db250ZW50ICRmaWxlDQogICAgfQ0KICAgIEVORCB7DQogICAgJGNvbnRlbnQgfCBBZGQtQ29udGVudCAkZmlsZQ0KICAgIH0NCn0NCkZ1bmN0aW9uIFdyaXRlLUNvbmZpZ3sNCiAgICAkZmlsZSA9ICcuXEhvTmZpZ3VyYXRvclxjb25maWdcbG9jYWxfY29uZmlnLmluaScNCgkkY2hlY2sgPSBUZXN0LVBhdGggJGZpbGUgLVBhdGhUeXBlIExlYWYNCglpZiAoJGNoZWNrIC1lcSAkZmFsc2UpIHsNCiAgICAgICAgY29weS1pdGVtIC1QYXRoICcuXEhvTmZpZ3VyYXRvclxjb25maWdcZGVmYXVsdF9jb25maWcuaW5pJyAgLURlc3RpbmF0aW9uICcuXEhvTmZpZ3VyYXRvclxjb25maWdcbG9jYWxfY29uZmlnLmluaScNCiAgICB9DQogICAgJElOSSA9IEdldC1Db250ZW50ICRmaWxlDQogICAgJEluaUhhc2ggPSBAe30NCiAgICAkSW5pVGVtcCA9IEAoKQ0KICAgIEZvckVhY2goJExpbmUgaW4gJElOSSkNCiAgICB7DQogICAgICAgICNXcml0ZS1Ib3N0KCRMaW5lKQ0KICAgICAgICBJZiAoJExpbmUgLW5lICIiIC1hbmQgJExpbmUuU3RhcnRzV2l0aCgiWyIpIC1uZSAkVHJ1ZSkNCiAgICAgICAgew0KICAgICAgICAgICAgJExpbmUgPSAkbGluZS5SZXBsYWNlKCcgPSAnLCc9JykNCiAgICAgICAgICAgICRJbmlUZW1wICs9ICRMaW5lDQogICAgICAgIH0NCiAgICB9DQogICAgRm9yRWFjaCgkTGluZSBpbiAkSW5pVGVtcCkgew0KICAgICAgICAkU3BsaXRBcnJheSA9ICRMaW5lLlNwbGl0KCI9IikNCiAgICAgICAgJEluaUhhc2ggKz0gQHskU3BsaXRBcnJheVswXSA9ICRTcGxpdEFycmF5WzFdfQ0KICAgICAgICB9DQogICAgJGluaUhhc2hbJ2hvbl9kaXJlY3RvcnknXT0kaG9uZGlyDQogICAgJHNiID0gTmV3LU9iamVjdCAtVHlwZU5hbWUgU3lzdGVtLlRleHQuU3RyaW5nQnVpbGRlcg0KICAgIGZvcmVhY2ggKCRuYW1lIGluICRJbmlIYXNoLktleXMpIHsNCiAgICAgICAgJHZhbHVlID0gJEluaUhhc2hbJG5hbWVdDQogICAgICAgICMgdGhlIHZhbHVlIG5lZWRzIHRvIGJlIHF1b3RlZCB3aGVuOg0KICAgICAgICAjIC0gaXQgYmVnaW5zIG9yIGVuZHMgd2l0aCB3aGl0ZXNwYWNlIGNoYXJhY3RlcnMNCiAgICAgICAgIyAtIGl0IGNvbnRhaW5zIHNpbmdsZSBvciBkb3VibGUgcXVvdGUgY2hhcmFjdGVycw0KICAgICAgICAjIC0gaXQgY29udGFpbnMgcG9zc2libGUgY29tbWVudCBjaGFyYWN0ZXJzICgnIycgb3IgJzsnKQ0KICAgICAgICBpZiAoJHZhbHVlIC1tYXRjaCAnXlxzK3xbIzsiJyddfFxzKyQnKSB7DQogICAgICAgICAgICAjIGVzY2FwZSBxdW90ZXMgaW5zaWRlIHRoZSB2YWx1ZSBhbmQgc3Vycm91bmQgdGhlIHZhbHVlIHdpdGggZG91YmxlIHF1b3RlIG1hcmtzDQogICAgICAgICAgICAkdmFsdWUgPSAnIicgKyAoJHZhbHVlIC1yZXBsYWNlICcoWyInJ10pJywgJ1wkMScpICsgJyInDQogICAgICAgIH0NCiAgICAgICAgW3ZvaWRdJHNiLkFwcGVuZExpbmUoIiRuYW1lID0gJHZhbHVlIikNCiAgICB9DQogICAgJHNiLlRvU3RyaW5nKCkgfCBPdXQtRmlsZSAkRmlsZQ0KICAgIFt2b2lkXSRzYi5DbGVhcigpDQogICAgIltPUFRJT05TXSIgfCBJbnNlcnQtQ29udGVudCAkZmlsZQ0KfQ0KDQpXcml0ZS1Ib3N0KCJDdXJyZW50IERpcmVjdG9yeTogJFBTU2NyaXB0Um9vdCIpDQpjZCAkUFNTY3JpcHRSb290DQojIyBJbnN0YWxsIENob2NvbGF0ZXkgcGFja2FnZSBtYW5hZ2VyICMjDQpTZXQtRXhlY3V0aW9uUG9saWN5IEJ5cGFzcyAtU2NvcGUgUHJvY2VzcyAtRm9yY2U7IFtTeXN0ZW0uTmV0LlNlcnZpY2VQb2ludE1hbmFnZXJdOjpTZWN1cml0eVByb3RvY29sID0gW1N5c3RlbS5OZXQuU2VydmljZVBvaW50TWFuYWdlcl06OlNlY3VyaXR5UHJvdG9jb2wgLWJvciAzMDcyOyBpZXggKChOZXctT2JqZWN0IFN5c3RlbS5OZXQuV2ViQ2xpZW50KS5Eb3dubG9hZFN0cmluZygnaHR0cHM6Ly9jb21tdW5pdHkuY2hvY29sYXRleS5vcmcvaW5zdGFsbC5wczEnKSkgMj4mMSB8IFdyaXRlLVZlcmJvc2UNCmNscw0KDQpXcml0ZS1PdXRwdXQgIg0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0NCkhvTmZpZ3VyYXRvciBBbGwgaW4gT25lIHNlcnZlciBpbnN0YWxsIHNjcmlwdA0KVGhlIGxhdW5jaGVyIHdpbGwgcnVuIG9uY2UgdGhlIGluc3RhbGwgaGFzIGNvbXBsZXRlZA0KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0NCiINCg0KIyMgSW5zdGFsbCByZXF1aXJlZCBzb2Z0d2FyZSB3aXRoIGNob2NvbGF0ZXkgLSB0aGlzIHdpbGwgYWxzbyBpbnN0YWxsIHRoZSBkZXBlbmRlbmNpZXMgZm9yIHRoZXNlIHByb2dyYW1zICMjDQpXcml0ZS1PdXRwdXQgIkluc3RhbGxpbmcgZGVwZW5kZW5jaWVzIGZyb20gQ2hvY29sYXRleSINCmNob2NvIGluc3RhbGwgcHl0aG9uMyAteSAyPiYxIHwgV3JpdGUtVmVyYm9zZSAgIyMgUHl0aG9uIDMgLSB0byBydW4gdGhlIEhvTmZpZ3VyYXRvciBsYXVuY2hlciBpbnN0YWxsDQpjaG9jbyBpbnN0YWxsIGdpdCAteSAyPiYxIHwgV3JpdGUtVmVyYm9zZSAjIyBHaXRodWIgQ2xpIC0gY2xvbmUgdGhlIHJlcXVpcmVkIHJlcG9zDQpjaG9jbyBpbnN0YWxsIG5zc20gLXkgMj4mMSB8IFdyaXRlLVZlcmJvc2UgIyMgTm9uLVN1Y2tpbmcgU2VydmljZSBNYW5hZ2VyIC0gZm9yIGF1dG9tYXRpbmcgc2VydmVyIHJlc3RhcnRzDQoNCiMjIFJlZnJlc2ggZW52aXJvbmVtbnQgdmFyaWFibGVzIGFmdGVyIGluc3RhbGxhdGlvbiBvZiBkZXBlbmRlbmNpZXMgIyMNCiRlbnY6Q2hvY29sYXRleUluc3RhbGwgPSBDb252ZXJ0LVBhdGggIiQoKEdldC1Db21tYW5kIGNob2NvKS5QYXRoKVwuLlwuLiIgICANCkltcG9ydC1Nb2R1bGUgIiRlbnY6Q2hvY29sYXRleUluc3RhbGxcaGVscGVyc1xjaG9jb2xhdGV5UHJvZmlsZS5wc20xIg0KcmVmcmVzaGVudiAyPiYxIHwgV3JpdGUtVmVyYm9zZQ0KDQojIyBDbG9uZSBIb05maWd1cmF0b3IgZmlsZXMgIyMNCldyaXRlLU91dHB1dCAiQ2xvbmluZyBIb05maWd1cmF0b3IgZmlsZXMiDQpnaXQgY2xvbmUgaHR0cHM6Ly9naXRodWIuY29tL2ZyYW5rdGhldGFuazAwMS9Ib05maWd1cmF0b3IgMj4mMSB8IFdyaXRlLVZlcmJvc2UNCg0KIyBhc2sgdG8gZG93bmxvYWQgSG9ODQokY29uZmlybWF0aW9uID0gUmVhZC1Ib3N0ICJEbyB5b3UgcmVxdWlyZSBhIGNsZWFuIEhvTiBkb3dubG9hZD8gKHkvbikiDQppZiAoJGNvbmZpcm1hdGlvbiAtZXEgJ3knKSB7DQogICAgIyMgRG93bmxvYWQgSG9OIGNsaWVudCAjIw0KICAgIFdyaXRlLU91dHB1dCAiRG93bmxvYWRpbmcgSG9OIENsaWVudCB0byBjdXJyZW50IGRpcmVjdG9yeS4gVGhpcyBtYXkgdGFrZSBzb21lIHRpbWUgLSA2LjNHQiINCiAgICAkVVJMPSJodHRwczovL2ZiLWRpcmVjdC5zdHJlYW1hbGwuZGF5L2FwaS9wdWJsaWMvZGwvZlgzV25CS2wiDQogICAgJEhPTj0iSGVyb2VzIG9mIE5ld2VydGggeDY0IC0gQ0xFQU4iDQogICAgJGhvbmRpcj0iJHB3ZFwkSE9OXCINCiAgICAkcHJvZ3Jlc3NQcmVmZXJlbmNlID0gJ3NpbGVudGx5Q29udGludWUnDQogICAgY3VybC5leGUgLUwgLW8gIiRIT04uemlwIiAkVVJMDQogICAgIyMgRXh0cmFjdCBIb04gQ2xpZW50ICMjDQogICAgV3JpdGUtT3V0cHV0ICJFeHRyYWN0aW5nIEhvTiBDbGllbnQgdG8gY3VycmVudCBkaXJlY3RvcnkiDQogICAgIyMgc2VydmVyIGJpbmFyeSBhZHZpc29yeQ0KICAgIEV4cGFuZC1BcmNoaXZlIC1QYXRoICIkSE9OLnppcCIgLURlc3RpbmF0aW9uUGF0aCAkcHdkIDI+JjEgfCBXcml0ZS1WZXJib3NlDQogICAgcm0gIiRIT04uemlwIg0KICAgIFdyaXRlLUNvbmZpZw0KICAgIFdyaXRlLUhvc3QoIlNlcnZlciBiaW5hcmllcyBtdXN0IGJlIG9idGFpbmVkIHlvdXJzZWxmIGFuZCBwbGFjZWQgaW4gJGhvbmRpciBiZWZvcmUgaG9zdGluZyBjYW4gb2NjdXIuIikNCn0NCiMgSW5zdGFsbCBweXRob24gcHJlLXJlcXVpc2l0ZXMNCldyaXRlLU91dHB1dCAiSW5zdGFsbGluZyBweXRob24gZGVwZW5kZW5jaWVzIg0KdHJ5IHsNCiAgICBweXRob24gLW0gcGlwIGluc3RhbGwgLS1wcmVmZXItYmluYXJ5IC1yIC5cSG9OZmlndXJhdG9yXGRlcGVuZGVuY2llc1xyZXF1aXJlbWVudHMudHh0IDI+JjEgfCBXcml0ZS1WZXJib3NlDQp9IGNhdGNoIHsNCiAgICBwaXAgaW5zdGFsbCAtLXByZWZlci1iaW5hcnkgLXIgLlxIb05maWd1cmF0b3JcZGVwZW5kZW5jaWVzXHJlcXVpcmVtZW50cy50eHQgMj4mMSB8IFdyaXRlLVZlcmJvc2UNCn0NCiRoZiA9IEdldC1Mb2NhdGlvbg0KJGhmID0gIiRoZlxIb05maWd1cmF0b3IiDQpjZCAkaGYNCldyaXRlLU91dHB1dCAiSG9uZmlndXJhdG9yIGRpcmVjdG9yeSBpcyAkaGYiDQpXcml0ZS1PdXRwdXQgIkhvTiBkaXJlY3RvcnkgaXMgJGhvbmRpciINCnRyeXsNCglTdGFydC1Qcm9jZXNzIGhvbmZpZ3VyYXRvci5leGUNCn0gY2F0Y2ggew0KCXB5dGhvbiBob25maWd1cmF0b3IucHkNCn0NCiRXc2hTaGVsbCA9IE5ldy1PYmplY3QgLWNvbU9iamVjdCBXU2NyaXB0LlNoZWxsDQokU2hvcnRjdXQgPSAkV3NoU2hlbGwuQ3JlYXRlU2hvcnRjdXQoIiV1c2VycHJvZmlsZSVcRGVza3RvcFxIb05maWd1cmF0b3IubG5rIikNCiRTaG9ydGN1dC5UYXJnZXRQYXRoID0gIiRwd2RcaG9uZmlndXJhdG9yLmV4ZSINCiRTaG9ydGN1dC5TYXZlKCkNCg0KV3JpdGUtT3V0cHV0ICJMYXVuY2hpbmcgSG9OZmlndXJhdG9yIC0geW91IG1heSBub3cgY2xvc2UgdGhpcyB3aW5kb3ciDQpwYXVzZQ== > tmp.txt
certutil -f -decode tmp.txt HoNfigurator-Installer.ps1
del tmp.txt
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File Honfigurator-Installer.ps1
pause
