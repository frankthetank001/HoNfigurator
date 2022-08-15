## Install Chocolatey package manager ##

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

## Install required software with chocolatey - this will also install the dependencies for these programs ##

choco install python3 -y  ## Python 3 - to run the HoNfigurator launcher install
choco install gh -y ## Github Cli - clone the required repos
choco install nssm -y ## Non-Sucking Service Manager - for automating server restarts

## Download HoN client ##

Write-Output "
-------------------------------------------

Downloading HoN Client to current directory
Please be patient - do NOT cancel

-------------------------------------------
"

$URL="https://store3.gofile.io/download/direct/a254d73c-9fe5-489f-85e5-92ac4bc6b084/HoN-Client-x64-CLEAN.zip"
$ZIP="HoN-Client-x64.zip"
$progressPreference = 'silentlyContinue'
Invoke-WebRequest -URI $URL -OutFile $ZIP


## Extract HoN Client ##

Write-Output "
------------------------------------------

Extracting HoN Client to current directory

------------------------------------------
"

Expand-Archive -Path $ZIP -DestinationPath $pwd
rm $ZIP
Write-Output "Extraction Complete - Script finished - WIP"
pause