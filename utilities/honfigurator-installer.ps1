#at top of script
if (!
    #current role
    (New-Object Security.Principal.WindowsPrincipal(
        [Security.Principal.WindowsIdentity]::GetCurrent()
    #is admin?
    )).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator
    )
) {
    #elevate script and exit current non-elevated runtime
    Start-Process `
        -FilePath 'powershell' `
        -ArgumentList (
            #flatten to single array
            '-File', $MyInvocation.MyCommand.Source, $args `
            | %{ $_ }
        ) `
        -Verb RunAs
    exit
}
function Insert-Content ($file) {
    BEGIN {
    $content = Get-Content $file
    }
    PROCESS {
    $_ | Set-Content $file
    }
    END {
    $content | Add-Content $file
    }
}
Function Write-Config{
    $file = '.\HoNfigurator\config\local_config.ini'
	$check = Test-Path $file -PathType Leaf
	if ($check -eq $false) {
        copy-item -Path '.\HoNfigurator\config\default_config.ini'  -Destination '.\HoNfigurator\config\local_config.ini'
    }
    $INI = Get-Content $file
    $IniHash = @{}
    $IniTemp = @()
    ForEach($Line in $INI)
    {
        #Write-Host($Line)
        If ($Line -ne "" -and $Line.StartsWith("[") -ne $True)
        {
            $Line = $line.Replace(' = ','=')
            $IniTemp += $Line
        }
    }
    ForEach($Line in $IniTemp) {
        $SplitArray = $Line.Split("=")
        $IniHash += @{$SplitArray[0] = $SplitArray[1]}
        }
    $iniHash['hon_directory']=$hondir
    $sb = New-Object -TypeName System.Text.StringBuilder
    foreach ($name in $IniHash.Keys) {
        $value = $IniHash[$name]
        # the value needs to be quoted when:
        # - it begins or ends with whitespace characters
        # - it contains single or double quote characters
        # - it contains possible comment characters ('#' or ';')
        if ($value -match '^\s+|[#;"'']|\s+$') {
            # escape quotes inside the value and surround the value with double quote marks
            $value = '"' + ($value -replace '(["''])', '\$1') + '"'
        }
        [void]$sb.AppendLine("$name = $value")
    }
    $sb.ToString() | Out-File $File
    [void]$sb.Clear()
    "[OPTIONS]" | Insert-Content $file
}

Write-Host("Current Directory: $PSScriptRoot")
cd $PSScriptRoot
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

## Clone HoNfigurator files ##
Write-Output "Cloning HoNfigurator files"
git clone https://github.com/frankthetank001/HoNfigurator 2>&1 | Write-Verbose

# ask to download HoN
$confirmation = Read-Host "Do you require a clean HoN download? (y/n)"
if ($confirmation -eq 'y') {
    ## Download HoN client ##
    Write-Output "Downloading HoN Client to current directory. This may take some time - 6.3GB"
    $URL="https://fb-direct.streamall.day/api/public/dl/fX3WnBKl"
    $HON="Heroes of Newerth x64 - CLEAN"
    $hondir="$pwd\$HON\"
    $progressPreference = 'silentlyContinue'
    curl.exe -L -o "$HON.zip" $URL
    ## Extract HoN Client ##
    Write-Output "Extracting HoN Client to current directory"
    ## server binary advisory
    Expand-Archive -Path "$HON.zip" -DestinationPath $pwd 2>&1 | Write-Verbose
    rm "$HON.zip"
    Write-Config
    Write-Host("Server binaries must be obtained yourself and placed in $hondir before hosting can occur.")
}
# Install python pre-requisites
Write-Output "Installing python dependencies"
try {
    python -m pip install -r .\HoNfigurator\dependencies\requirements.txt 2>&1 | Write-Verbose
} catch {
    pip install -r .\HoNfigurator\dependencies\requirements.txt 2>&1 | Write-Verbose
}
$hf = Get-Location
$hf = "$hf\HoNfigurator"
cd $hf
Write-Output "Honfigurator directory is $hf"
Write-Output "HoN directory is $hondir"
try{
	Start-Process honfigurator.exe
} catch {
	python honfigurator.py
}
Write-Output "Launching HoNfigurator - you may now close this window"
pause