# Restart this script in elevated mode if this user is not an administrator.
# ULTRA SUPER NON POWERSHELL-LIKE CODE AHEAD
# -------------------------------------------------------------------------
[Threading.Thread]::GetDomain().SetPrincipalPolicy([Security.Principal.PrincipalPolicy]::WindowsPrincipal)
$thread_security_principal = `
  [Security.Principal.WindowsPrincipal]([Threading.Thread]::CurrentPrincipal)
if ( -NOT $thread_security_principal.IsInRole("Administrators") ) {
    $argv = @($MyInvocation.MyCommand.Definition) + $args
    start-process "powershell.exe" -Arg $argv -Verb RunAs
    exit 2
}
echo $PSScriptRoot
cd $PSScriptRoot

$file = '.\config\local_config.ini'
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

ForEach($Line in $IniTemp)
{
$SplitArray = $Line.Split("=")
$IniHash += @{$SplitArray[0] = $SplitArray[1]}
}
1..$IniHash.svr_total | % {
    $exe = "KONGOR_ARENA_$_.exe"
    $result=.\dependencies\server_exe\pingplayerconnected-DC.exe $exe
    write-host($exe +" = " + $result)
}
Read-Host -Prompt "Press any key to continue"