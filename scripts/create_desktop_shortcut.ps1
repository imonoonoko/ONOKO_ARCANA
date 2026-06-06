param(
  [string] $DesktopPath = [Environment]::GetFolderPath("Desktop")
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$ElectronExe = Join-Path $Root "web-app\node_modules\electron\dist\electron.exe"
$EntryPoint = Join-Path $Root "web-app\electron\main.cjs"
$WorkingDirectory = Join-Path $Root "web-app"
$IconPath = Join-Path $Root "assets\generated\app-icons\onoko-arcana-app-icon-v1.ico"
$ShortcutPath = Join-Path $DesktopPath "ONOKO ARCANA.lnk"

foreach ($Required in @($ElectronExe, $EntryPoint, $WorkingDirectory, $IconPath)) {
  if (!(Test-Path -LiteralPath $Required)) {
    throw "Missing required file: $Required"
  }
}

New-Item -ItemType Directory -Force -Path $DesktopPath | Out-Null

$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ElectronExe
$Shortcut.Arguments = "`"$EntryPoint`""
$Shortcut.WorkingDirectory = $WorkingDirectory
$Shortcut.IconLocation = "$IconPath,0"
$Shortcut.Description = "Launch ONOKO ARCANA desktop reading table"
$Shortcut.WindowStyle = 1
$Shortcut.Save()

[PSCustomObject]@{
  ok = $true
  shortcut = $ShortcutPath
  target = $Shortcut.TargetPath
  arguments = $Shortcut.Arguments
  icon = $Shortcut.IconLocation
} | ConvertTo-Json
