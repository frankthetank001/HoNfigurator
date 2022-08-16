## Install Chocolatey package manager ##
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

## Install required software with chocolatey - this will also install the dependencies for these programs ##
choco install python3 -y  ## Python 3 - to run the HoNfigurator launcher install
choco install git -y ## Github Cli - clone the required repos
choco install nssm -y ## Non-Sucking Service Manager - for automating server restarts
refreshenv

## Download HoN client ##
Write-Output "-Downloading HoN Client to current directory
Please be patient - do NOT cancel"
$URL="https://store3.gofile.io/download/direct/a254d73c-9fe5-489f-85e5-92ac4bc6b084/HoN-Client-x64-CLEAN.zip"
$ZIP="HoN-Client-x64.zip"
$progressPreference = 'silentlyContinue'
Invoke-WebRequest -URI $URL -OutFile $ZIP

## Extract HoN Client ##
Write-Output "-Extracting HoN Client to current directory"
Expand-Archive -Path $ZIP -DestinationPath $pwd
rm $ZIP
Write-Output "Cloning server binaries from external github"

## Clone the Server Binaries and copy to HoN directory ##
$WS=".\wasserver\"
$HON=".\HoN-Client-x64-CLEAN\"
git clone https://github.com/wasserver/wasserver
cp $WS\hon_x64.exe, $WS\k2_x64.dll -Destination "$HON"
cp $WS\cgame_x64.dll, $WS\game_shared_x64.dll, $WS\game_x64.dll -Destination "$HON\game"
rm $WS -r -force

## Clone HoNfigurator files ##
$hondir=Get-Location
git clone https://github.com/frankthetank001/HoNfigurator
pip install -r .\HoNfigurator\dependencies\requirements.txt
ac -Path .\HoNfigurator\config\default_config.ini -Value "
hon_directory = $hondir\HoN-Client-x64-CLEAN\"
py .\HoNfigurator\honfigurator.py


Write-Output "-Launching HoNfigurator - you may now close this window"
pause
