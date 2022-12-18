param (
    [switch]$reset = $false,
    [switch]$launch = $false
)

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

Write-Host("Current Directory: $PSScriptRoot")
# if (-Not $PSBoundParameters.ContainsKey('launch')) {
# 	Write-Host("Please only launch this script using the current 'Install-Beats.bat'. Otherwise this script may be an outdated version. Closing.")
# 	Read-Host("press any key to exit")
# 	Exit
# }
cd $PSScriptRoot
## Install Chocolatey package manager ##
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) 2>&1 | Write-Verbose
cls

Write-Host("============================================================================================================`n
Installing Filebeat and Metric beat using Official Chocolatey, please wait")
choco install filebeat -y 2>&1 | Write-Verbose
choco install metricbeat -y 2>&1 | Write-Verbose
choco install yq -y 2>&1 | Write-Verbose
choco install openssl -y 2>&1 | Write-Verbose

## Refresh environemnt variables after installation of dependencies ##
$env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."   
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
refreshenv 2>&1 | Write-Verbose

metricbeat --path.home (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools') modules enable system 2>&1 | Write-Verbose

function Read-Config {
    if ($env:HONFIGURATOR_DIR) {
        $file = "$env:HONFIGURATOR_DIR\config\local_config.ini"
    } else {
        $file = '..\config\local_config.ini'
    }
	$check = Test-Path $file -PathType Leaf
	if ($check -eq $false) {
        return $check
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
    return $IniHash
    #$iniHash['hon_directory']=$hondir
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
function Write-Config ($api_key) {
    $file = '..\config\local_config.ini'
    $local_config['api_key']=$api_key
    $sb = New-Object -TypeName System.Text.StringBuilder
    foreach ($name in $local_config.Keys) {
        $value = $local_config[$name]
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

function Check-Cert {
    $check = Test-Path -Path $filebeat_client_pem
    if ($check -eq $false) {
        $key = Test-Path -Path $filebeat_client_key
        if ($key -eq $false) { 
            openssl req -newkey rsa:2048 -keyout $filebeat_client_key -out "$env:USERPROFILE\Desktop\client.csr" -nodes -subj "/CN=$hoster-Beats-Client"
            Copy-Item -Path $filebeat_client_key -Destination $metricbeat_client_key
            Write-Host("Key created in: `n$filebeat_client_key`n$metricbeat_client_key")
        }
        Write-Host("============================================================================================================`n
Please provide generated CSR file ($env:USERPROFILE\Desktop\client.csr) to @FrankTheGodDamnMotherFuckenTank

You will then receive client.pem file. Please copy this file into the following directories:`n$filebeat_client_pem`n$metricbeat_client_pem
============================================================================================================`n")
        Read-Host("Press any key once the files have been copied")
        Check-Cert
    } else {
        Copy-Item -Path $filebeat_client_pem -Destination $metricbeat_client_pem
        Write-Host("Restarting Filebeat")
        Restart-Service -Name "filebeat"
        Write-Host("Restarting MetricBeat")
        Restart-Service -Name "metricbeat"
    }
}
function Setup-Beats {
    while ($launcher -notin ("HoNfigurator","COMPEL")) {
        $launcher=Read-Host("Enter 1 if using HoNfigurator. Enter 2 if using COMPEL")
        if ($launcher -eq "1") { $launcher = "HoNfigurator"} elseif ($launcher -eq "2") { $launcher = "COMPEL"}
    }
    if ($launcher -eq "HoNfigurator"){
        Write-Host("Reading data from existing HoNfigurator config file")
        $local_config = Read-Config
        if ($local_config) {
                $log_paths = "$($local_config['hon_directory'])..\hon_server_instances\Hon_Server_*\Documents\Heroes of Newerth x64\game\logs\*.clog"
        } else {
            Write-Host("Make sure you have at least configured some servers and are running this script from the HoNfigurator\Utilities folder.")
            return
        }
        $cores = $local_config['core_assignment']
        $hoster = $local_config['svr_hoster']
        $region = $local_config['svr_region_short']
    } else {
        $cores = "one core/server"
        $confirm = $false
        if ($env:BeatsHoster) {
            Write-Host("Compel settings from last run are:
            Server Name: $env:BeatsHoster
            Server Region: $env:BeatsRegion
            Log Directory: $env:BeatsLogDir
            ")
            $check_confirm = $false
            while ($check_confirm -eq $false) {
                $confirm = Read-Host("Is this correct? (y/n)")
                if ($confirm -eq "y" -or $confirm -eq "Y") {
                    $confirm = $true
                    $check_confirm = $true
                }
                elseif ($confirm -eq "n" -or $confirm -eq "N") {
                    $confirm = $false
                    $check_confirm = $true}
                else { Write-Host("Please enter Y or N. $confirm is not valid.") }
            }
        }
        if ($null -eq $confirm -or $confirm -eq $false) {
            $hoster = ((Read-Host 'Please enter server name. Make sure that this is accurate as what is in COMPEL') -replace '"')
            [System.Environment]::SetEnvironmentVariable('BeatsHoster',$hoster,[System.EnvironmentVariableTarget]::Machine)
            $region = ((Read-Host 'Please enter server region. Make sure that this is accurate as what is in COMPEL') -replace '"')
            [System.Environment]::SetEnvironmentVariable('BeatsRegion',$region,[System.EnvironmentVariableTarget]::Machine)
            $check = $false
            while ($check -eq $false) {
                $logdir = ((Read-Host 'Enter logs folder path (Example: C:\Users\honserver4\AppData\Local\Temp\HON\DOCUMENTS\HEROES OF NEWERTH x64\GAME\logs') -replace '"')
                $check = Test-Path -Path $logdir
                if ($check -eq $false) {Write-Host("The directory entered does not exist. Please try again.")}
            }
            [System.Environment]::SetEnvironmentVariable('BeatsLogDir',$logdir,[System.EnvironmentVariableTarget]::Machine)
        } else {
            $hoster = $env:BeatsHoster
            $region = $env:BeatsRegion
            $logdir = $env:BeatsLogDir
        }
        $log_paths = "$logdir\*.clog
      - $logdir\..\console.log"
    }
    $discord_name = $null
    if ($env:BeatsAdmin) {
        $confirm = $false
        while ($confirm -notin ("y","n","yes","no")) {
            $confirm = Read-Host("Is the server admin still $env:BeatsAdmin ? (y/n)")
        }
        if ($confirm -in ("y","yes")) {
            $discord_name = $env:BeatsAdmin
        }
    }
    if ($null -eq $discord_name) {
        $discord_name = Read-Host("Please enter your Discord username. This is so owners of servers are contactable. Example: kladze#0589") 
        [System.Environment]::SetEnvironmentVariable('BeatsAdmin',$discord_name,[System.EnvironmentVariableTarget]::Machine)
    }
    # $email = $null
    # if ($env:BeatsEmail) {
    #     $confirm = $false
    #     while ($confirm -notin ("y","n","yes","no")) {
    #         $confirm = Read-Host("Is the alert email still $env:BeatsEmail ? (y/n)")
    #     }
    #     if ($confirm -in ("y","yes")) {
    #         $email = $env:BeatsEmail
    #     }
    # }
    # if ($null -eq $email) { 
    #     $email = Read-Host("Enter your email if you want to be sent alerts in the future (optional)")
    #     [System.Environment]::SetEnvironmentVariable('BeatsEmail',$email,[System.EnvironmentVariableTarget]::Machine)
    # }

    # check if -reset parameter has been passed. If so, clear the filebeat registry to re-ingest data
    if ($PSBoundParameters.ContainsKey('reset')) {
        Stop-Service -Name 'filebeat'
        Write-Host("Clearing registry data, so we can re-ingest from the start..")
        $path_to_remove = "$ENV:ProgramData\filebeat\registry"
        Remove-Item $path_to_remove -Recurse -Force
    }
    $check = Test-Path "honfigurator-chain.pem" -PathType Leaf
    if ($check -eq $false) {
	    curl.exe -o honfigurator-chain.pem https://honfigurator.app/honfigurator-chain.pem
    }
    $filebeat_chain = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\honfigurator-chain.pem')
    $filebeat_client_pem = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\client.pem')
    $filebeat_client_key = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\client.key')
    $metricbeat_chain = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\honfigurator-chain.pem')
    $metricbeat_client_pem = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\client.pem')
    $metricbeat_client_key = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\client.key')

    New-Item (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs') -ItemType Directory -ErrorAction SilentlyContinue
    New-Item (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs') -ItemType Directory -ErrorAction SilentlyContinue

    Copy-Item -Path .\honfigurator-chain.pem -Destination $filebeat_chain
    Copy-Item -Path .\honfigurator-chain.pem -Destination $metricbeat_chain

    $TargetConfig = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\filebeat.yml')
    $Services = "filebeat.inputs:
  - type: filestream
    id: hon-logs-$hoster
    enabled: true
    paths:
      - $log_paths
    encoding: utf-16le
    close_inactive: 15m
    exclude_files: '[`".gz$`"]'
    fields_under_root: true
    fields:
      Server:
        Name: $hoster
        Launcher: $launcher
        Admin: $discord_name
        Region: $region
        Affinity: $cores
"
    if ($launcher -eq "HoNfigurator") {
        $services = $services + 
"  - type: filestream
    id: honfigurator-logs-$hoster
    enabled: true
    paths:
      - $($local_config['hon_directory'])\..\hon_server_instances\Hon_Server_*\Documents\Heroes of Newerth x64\game\logs\adminbot*\adminbot*.log
    close_inactive: 15m
    exclude_files: '[`".gz$`"]'
    parsers:
    - multiline:
        type: pattern
        pattern: '.*Traceback|^\s'
        negate: false
        match: after
        multiline.flush_pattern: '\['
    fields_under_root: true
    fields:
      Server:
        Name: $hoster
        Launcher: $launcher
        Admin: $discord_name
        Region: $region
        Affinity: $cores
"
}
    $services = $services +
"filebeat.config.modules:
  path: `${path.config}/modules.d/*.yml
  reload.enabled: false
setup.template.settings:
  index.number_of_shards: `"1`"
output.logstash:
  hosts: hon-elk.honfigurator.app:5044
  ssl.certificate_authorities: $filebeat_chain
  ssl.certificate: $filebeat_client_pem
  ssl.key: $filebeat_client_key
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_locale: ~
"
    $Services | ConvertTo-Json -Depth 100 | &'yq' eval - --prettyPrint | Out-File $TargetConfig -Encoding UTF8

    $TargetConfig = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\metricbeat.yml')
    $services = "metricbeat.config.modules:
  path: `${path.config}/modules.d/*.yml
  reload.enabled: null
setup.template.settings:
  index.number_of_shards: 1
  index.codec: best_compression
fields_under_root: true
fields:
  Server:
    Name: $hoster
    Launcher: $launcher
    Admin: $discord_name
    Region: $region
setup.dashboards.enabled: false
output.logstash:
  hosts: 'hon-elk.honfigurator.app:5044'
  ssl.certificate_authorities: $metricbeat_chain
  ssl.certificate: $metricbeat_client_pem
  ssl.key: $metricbeat_client_key
processors:
  - add_host_metadata: ~
  - add_locale: ~
"
    # $Services = [pscustomobject]@{
    #     'metricbeat.config.modules' =
    #         [ordered]@{
    #             'path' = '${path.config}/modules.d/*.yml'
    #             'reload.enabled' = $false1
    #         }
    #     'setup.template.settings' =
    #         [ordered]@{
    #             'index.number_of_shards' = '1'
    #             'index.codec' = 'best_compression'
    #         }
    #     'fields_under_root' = $true
    #     'fields' = [ordered]@{
    #         'Server' = [ordered]@{
    #             'Name' = $local_config['svr_hoster']
    #             'Launcher' = $launcher
    #             'Region' = $local_config['svr_region_short']
    #         }
    #     }
    #     'setup.dashboards.enabled' = $false
    #     'output.elasticsearch' =
    #         [ordered]@{
    #             'hosts' = '[hon-elk.honfigurator.app:9200]'
    #             'protocol' = 'https'
    #             'api_key' = $api_key
    #             'ssl.certificate_aurhotities' = '[C:\ProgramData\Elastic\Beats\filebeat\certs\client.pem,C:\ProgramData\Elastic\Beats\filebeat\certs\chain.pem]'
    #             'ssl.certificate' = 'C:\ProgramData\Elastic\Beats\filebeat\certs\client.pem'
    #             'ssl.key' = 'C:\ProgramData\Elastic\Beats\filebeat\certs\client.key'
    #         }
        
    #     'processors' = @(
    #         [ordered]@{
    #             'add_host_metadata' = '~'
    #         }
    #     )
    # }
    $Services | ConvertTo-Json -Depth 100 | &'yq' eval - --prettyPrint | Out-File $TargetConfig -Encoding UTF8

    $TargetConfig = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\modules.d\system.yml')
    $Services = "# Module: system
    # Docs: https://www.elastic.co/guide/en/beats/metricbeat/8.4/metricbeat-module-system.html
    - module: system
      period: 10s
      metricsets:
        - cpu
        #- load
        - memory
        - network
        - process
        - process_summary
        - socket_summary
        #- entropy
        - core
        - diskio
        #- socket
        #- service
        #- users
      process.include_top_n:
        by_cpu: 5      # include top 5 processes by CPU
        by_memory: 5   # include top 5 processes by memory
    - module: system
      period: 1m
      metricsets:
        - filesystem
        - fsstat
      processors:
      - drop_event.when.regexp:
          system.filesystem.mount_point: '^/(sys|cgroup|proc|dev|etc|host|lib|snap)($|/)'
    - module: system
      period: 15m
      metricsets:
        - uptime"
    $Services | ConvertTo-Json -Depth 100 | &'yq' eval - --prettyPrint | Out-File $TargetConfig -Encoding UTF8
    Check-Cert
    Write-Host("success!")
}
Setup-Beats