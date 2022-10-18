param (
    [switch]$reset = $false
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

metricbeat --path.home (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools') modules enable system

function Read-Config {
    $file = '..\config\local_config.ini'
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
            openssl req -newkey rsa:2048 -keyout $filebeat_client_key -out $filebeat_client_csr -nodes -subj "/CN=$hoster-Beats-Client"
            Copy-Item -Path $filebeat_client_key -Destination $metricbeat_client_key
            Write-Host("Key created in: `n$filebeat_client_key`n$metricbeat_client_key")
        }
        Write-Host("============================================================================================================`n
Please provide generated CSR file ($filebeat_client_csr) to @FrankTheGodDamnMotherFuckenTank

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
    $launcher=Read-Host("Enter 1 if using HoNfigurator. Enter 2 if using COMPEL")
    if ($launcher -eq "1") { $launcher = "HoNfigurator"} else { $launcher = "COMPEL"}
    if ($launcher -eq "HoNfigurator"){
        $local_config = Read-Config
        if ($local_config) {
            if ($local_config['hon_directory']) {
                $path_slave = $local_config['hon_directory']+"..\hon_server_instances\Hon_Server_*\Documents\Heroes of Newerth x64\game\logs\*.clog"
                $path_match = $local_config['hon_directory']+"..\hon_server_instances\Hon_Server_*\Documents\Heroes of Newerth x64\game\logs\M*.log"
            } else {
                Write-Host("Make sure you have at least configured some servers and are running this script from the HoNfigurator\Utilities folder.")
                return
            }
            $hoster = $local_config['svr_hoster']
            $region = $local_config['svr_region_short']
        }
    } else {
        $hoster = ((Read-Host 'Please enter server name. Make sure that this is accurate as what is in COMPEL') -replace '"')
        $region = ((Read-Host 'Please enter server region. Make sure that this is accurate as what is in COMPEL') -replace '"')
        $check = $false
        while ($check -eq $false) {
            $logdir = ((Read-Host 'Enter logs folder path') -replace '"')
            $check = Test-Path -Path $logdir
            if ($check -eq $false) {Write-Host("The directory entered does not exist. Please try again.")}
        }
        $path_slave = "$logdir\*.clog"
        $path_match = "$logdir\M*.log"
    }
    # check if -reset parameter has been passed. If so, clear the filebeat registry to re-ingest data
    if ($reset) {
        Stop-Service -Name 'filebeat'
        Write-Host("Clearing registry data, so we can re-ingest from the start..")
        $path_to_remove = "$ENV:ProgramData\filebeat\registry"
        Remove-Item $path_to_remove -Recurse -Force
    }

    $filebeat_chain = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\honfigurator-chain.pem')
    $filebeat_client_pem = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\client.pem')
    $filebeat_client_key = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\client.key')
    $filebeat_client_csr = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs\client.csr')
    $metricbeat_chain = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\honfigurator-chain.pem')
    $metricbeat_client_pem = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\client.pem')
    $metricbeat_client_key = (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs\client.key')

    New-Item (Join-Path $ENV:ProgramData 'chocolatey\lib\metricbeat\tools\certs') -ItemType Directory -ErrorAction SilentlyContinue
    New-Item (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\certs') -ItemType Directory -ErrorAction SilentlyContinue

    Copy-Item -Path .\honfigurator-chain.pem -Destination $filebeat_chain
    Copy-Item -Path .\honfigurator-chain.pem -Destination $metricbeat_chain

    $TargetConfig = (Join-Path $ENV:ProgramData 'chocolatey\lib\filebeat\tools\filebeat.yml')
    $Services = [pscustomobject]@{
        'filebeat.inputs' = @(
            [ordered]@{
                'type' =  'filestream'
                'id' = "hon-logs-$hoster"
                'enabled' = $true
                'paths' = @(
                    $path_slave
                    $path_match
                )
                'encoding' = 'utf-16le'
                'exclude_files' = '[".gz$"]'
                'multiline.pattern' = '^\d\d\'
                'multiline.negate' = $true
                'multiline.match' = 'after'
                'fields_under_root' = $true
                'fields' = [ordered]@{
                    'Server' = [ordered]@{
                        'Name' = $hoster
                        'Launcher' = $launcher
                        'Region' = $region
                    }
                }
            }
        )
        'filebeat.config.modules' =
            [ordered]@{
                'path' = '${path.config}/modules.d/*.yml'
                'reload.enabled' = $false
            }
        'setup.template.settings' =
            [ordered]@{
                'index.number_of_shards' = '1'
            }
        'output.logstash' =
            [ordered]@{
                'hosts' = 'hon-elk.honfigurator.app:5044'
                'ssl.certificate_authorities' = $filebeat_chain
                'ssl.certificate' = $filebeat_client_pem
                'ssl.key' = $filebeat_client_key
            }
        
        'processors' = @(
            [ordered]@{
                'add_host_metadata' = [ordered]@{
                    'when.not.contains.tags' = 'forwarded'
                }
            }
        )
    }
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
    Region: $region
setup.dashboards.enabled: false
output.logstash:
  hosts: 'hon-elk.honfigurator.app:5044'
  ssl.certificate_authorities: $metricbeat_chain
  ssl.certificate: $metricbeat_client_pem
  ssl.key: $metricbeat_client_key
processors:
  - add_host_metadata: ~
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
    Read-Host("Success! Press any key to close.")
}
Setup-Beats