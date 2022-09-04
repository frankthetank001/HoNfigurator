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
Write-Host("Current Directory: $PSScriptRoot")
cd $PSScriptRoot
$limit = (Get-Date).AddDays(-15)
function Remove-Logs
{
    $logs = "$_\Documents\Heroes of Newerth x64\game\logs\"
    $replays = "$_\Documents\Heroes of Newerth x64\game\replays\"
    $replays = "$_\Documents\Heroes of Newerth x64\game\replays\"
    write-host ("cleaning logs... $logs")
    write-host ("cleaning replays... $replays")
    Get-ChildItem -Path $logs -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} | Remove-Item -Force
    Get-ChildItem -Path $replays -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} |  Remove-Item -Force
    Get-ChildItem -Path $diagnostics -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} |  Remove-Item -Force

    # Delete any empty directories left behind after deleting the old files.
    Get-ChildItem -Path $logs -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -Force -Recurse
    Get-ChildItem -Path $replays -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -Force -Recurse
    Get-ChildItem -Path $diagnostics -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -Force -Recurse
}

function Remove-Logs-View {
    $logs = "$_\Documents\Heroes of Newerth x64\game\logs\"
    $diagnostics = "$_\Documents\Heroes of Newerth x64\game\logs\diagnostics"
    $replays = "$_\Documents\Heroes of Newerth x64\game\replays\"
    Get-ChildItem -Path $logs -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} | Remove-Item -WhatIf -Force
    Get-ChildItem -Path $replays -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} |  Remove-Item -WhatIf -Force
    Get-ChildItem -Path $diagnostics -Force | Where-Object { !$_.PSIsContainer -and $_.LastWriteTime -lt $limit} |  Remove-Item -WhatIf -Force

    # Delete any empty directories left behind after deleting the old files.
    Get-ChildItem -Path $logs -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -WhatIf -Force -Recurse
    Get-ChildItem -Path $replays -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -WhatIf -Force -Recurse
    Get-ChildItem -Path $diagnostics -Force | Where-Object { $_.PSIsContainer -and (Get-ChildItem -Path $_.FullName -Recurse -Force | Where-Object { !$_.PSIsContainer }) -eq $null} | Remove-Item -WhatIf -Force -Recurse
}

$dir = Get-ChildItem '.\hon_server_*' | ? {$_.PSIsContainer}

$confirmation = Read-Host "Do you want to clean files or view what would be deleted first? (delete/view)"
if ($confirmation -eq 'view') {
    write-host("=======================================================================")
    write-host("viewing files older than $limit")
    $dir | ForEach-Object {Set-Location $_.FullName;Remove-Logs-View}
    write-host("=======================================================================")
}
elseif ($confirmation -eq 'delete') {
    write-host("=======================================================================")
    write-host("deleting files older than $limit")
    $dir | ForEach-Object {Set-Location $_.FullName;Remove-Logs}
    write-host("=======================================================================")
} else {
    write-host("=======================================================================")
    write-host("Not a valid input. Please try again.")
    write-host("=======================================================================")
}
Read-Host("Press any key to continue")