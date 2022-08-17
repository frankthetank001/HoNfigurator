## Install Chocolatey package manager ##
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) 2>&1 | Write-Verbose
cls

Write-Output "
-----------------------------------------------------
HoNfigurator All in One server install script
The launcher will run once the install has completed
-----------------------------------------------------
"

## Install required software with chocolatey - this will also install the dependencies for these programs ##
Write-Output "Installing dependencies from Chocolatey"
choco install python3 -y 2>&1 | Write-Verbose  ## Python 3 - to run the HoNfigurator launcher install
choco install git -y 2>&1 | Write-Verbose ## Github Cli - clone the required repos
choco install nssm -y 2>&1 | Write-Verbose ## Non-Sucking Service Manager - for automating server restarts

## Refresh environemnt variables after installation of dependencies ##
$env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."   
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
refreshenv 2>&1 | Write-Verbose

## Download HoN client ##
Write-Output "Downloading HoN Client to current directory. This may take some time - 6.3GB"
$URL="https://store3.gofile.io/download/direct/a254d73c-9fe5-489f-85e5-92ac4bc6b084/HoN-Client-x64-CLEAN.zip"
$ZIP="HoN-Client-x64.zip"
$progressPreference = 'silentlyContinue'
Invoke-WebRequest -URI $URL -OutFile $ZIP

## Extract HoN Client ##
Write-Output "Extracting HoN Client to current directory"
Expand-Archive -Path $ZIP -DestinationPath $pwd 2>&1 | Write-Verbose
rm $ZIP

## Clone the Server Binaries and copy to HoN directory ##
Write-Output "Cloning server binaries from external github"
$WS=".\wasserver\"
$HON=".\HoN-Client-x64-CLEAN\"
git clone https://github.com/wasserver/wasserver 2>&1 | Write-Verbose
cp $WS\hon_x64.exe, $WS\k2_x64.dll -Destination "$HON"
cp $WS\cgame_x64.dll, $WS\game_shared_x64.dll, $WS\game_x64.dll -Destination "$HON\game"
rm $WS -r -force

## Clone HoNfigurator files ##
Write-Output "Cloning HoNfigurator files"
$hondir=Get-Location
git clone https://github.com/frankthetank001/HoNfigurator 2>&1 | Write-Verbose
Write-Output "Installing python dependencies"
pip install -r .\HoNfigurator\dependencies\requirements.txt 2>&1 | Write-Verbose
ac -Path .\HoNfigurator\config\default_config.ini -Value "
hon_directory = $hondir\HoN-Client-x64-CLEAN\"
py .\HoNfigurator\honfigurator.py
Write-Output "Launching HoNfigurator - you may now close this window"
pause
