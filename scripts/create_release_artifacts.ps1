param(
  [string] $Version
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$PackageJsonPath = Join-Path $Root "web-app\package.json"
$PackageJson = Get-Content -LiteralPath $PackageJsonPath -Raw | ConvertFrom-Json

if ([string]::IsNullOrWhiteSpace($Version)) {
  $Version = "v$($PackageJson.version)"
}

if ($Version -notmatch "^v\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?$") {
  throw "Version must look like v0.1.1, got: $Version"
}

$Dist = Join-Path $Root "dist"
$PackageRoot = Join-Path $Dist "onoko-arcana-local"
$ArtifactDir = Join-Path $Dist "release-artifacts"
$ZipName = "onoko-arcana-$Version-local.zip"
$ZipPath = Join-Path $ArtifactDir $ZipName
$ShaPath = "$ZipPath.sha256"
$InstallerName = "onoko-arcana-$Version-setup.exe"
$BuiltInstallerPath = Join-Path $Dist "installer\$InstallerName"
$InstallerPath = Join-Path $ArtifactDir $InstallerName
$InstallerShaPath = "$InstallerPath.sha256"

if (!(Test-Path -LiteralPath $PackageRoot)) {
  throw "Local package does not exist. Run npm run package:local first."
}

if (!(Test-Path -LiteralPath $BuiltInstallerPath)) {
  throw "Installer package does not exist. Run npm run package:installer first: $BuiltInstallerPath"
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null
Remove-Item -LiteralPath $ZipPath, $ShaPath, $InstallerPath, $InstallerShaPath -Force -ErrorAction SilentlyContinue

Compress-Archive -Path (Join-Path $PackageRoot "*") -DestinationPath $ZipPath -Force
Copy-Item -LiteralPath $BuiltInstallerPath -Destination $InstallerPath -Force

Add-Type -AssemblyName System.IO.Compression.FileSystem
$Zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $ZipPath))
try {
  $Entries = $Zip.Entries.FullName | ForEach-Object { $_ -replace "\\", "/" }
  $RequiredEntries = @(
    "START_ONOKO_ARCANA.cmd",
    "CREATE_DESKTOP_SHORTCUT.ps1",
    "package-manifest.json",
    "LICENSE",
    "SECURITY.md",
    "DISTRIBUTION_NOTICE.md",
    "docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md",
    "assets/generated/app-icons/onoko-arcana-app-icon-v1.ico",
    "assets/generated/app-icons/onoko-arcana-app-icon-v1.png"
  )
  foreach ($Entry in $RequiredEntries) {
    if ($Entries -notcontains $Entry) {
      throw "Release zip is missing required entry: $Entry"
    }
  }

  $ForbiddenEntries = @(
    "assets/generated/app-icons/onoko-arcana-app-icon-v1-alpha-raw.png",
    "assets/generated/app-icons/onoko-arcana-app-icon-v1-source-chromakey.png"
  )
  foreach ($Entry in $ForbiddenEntries) {
    if ($Entries -contains $Entry) {
      throw "Release zip contains non-runtime icon source material: $Entry"
    }
  }
}
finally {
  $Zip.Dispose()
}

$Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $ZipPath).Hash
"$Hash  $ZipName" | Set-Content -LiteralPath $ShaPath -Encoding ascii
$InstallerHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $InstallerPath).Hash
"$InstallerHash  $InstallerName" | Set-Content -LiteralPath $InstallerShaPath -Encoding ascii

[PSCustomObject]@{
  ok = $true
  version = $Version
  installer = (Resolve-Path $InstallerPath).Path
  installerSha256 = $InstallerHash
  installerSha256File = (Resolve-Path $InstallerShaPath).Path
  zip = (Resolve-Path $ZipPath).Path
  sha256 = $Hash
  sha256File = (Resolve-Path $ShaPath).Path
} | ConvertTo-Json
