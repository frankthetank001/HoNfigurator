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
echo $PSScriptRoot
cd $PSScriptRoot

$file = '..\config\local_config.ini'
#Write-Host ('This is the raw INI file contents: ')
#Write-Host
$INI = Get-Content $file
#$Ini

$IniHash = @{}
$IniTemp = @()
ForEach($Line in $INI)
{
    If ($Line -ne "" -and $Line.StartsWith("[") -ne $True)
    {
        $Line = $line.Replace(' = ','=')
        $IniTemp += $Line
    }
}
# Write-Host
# Write-Host('=============================================')
# Write-Host
# Write-Host ('This is what has been added to $IniTemp after filtering')
# Write-Host
# $IniTemp

# Write-Host
# Write-Host('===============================================')
# Write-Host
# Write-Host('Here is the hash table:')
# Write-Host

Function Player-Count{
ForEach($Line in $IniTemp)
    {
    $SplitArray = $Line.Split("=")
    $IniHash += @{$SplitArray[0] = $SplitArray[1]}
    }
    1..$IniHash.svr_total | % {
        $exe = "KONGOR_ARENA_$_.exe"
        $result=..\dependencies\server_exe\pingplayerconnected-DC.exe $exe
        write-host($exe +" = " + $result)
    }
    Read-Host -Prompt "Press any key to check again"
    Player-Count
}
Player-Count