# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Packages the repository into dist/cse305_hwNN_231805033_231805026.zip excluding build, VCS, runtime DB, virtualenv, and IDE artifacts.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$HomeworkNumber = '01'
)

$ErrorActionPreference = 'Stop'

if ($HomeworkNumber -match '^\d$') {
    $nn = "0$HomeworkNumber"
} elseif ($HomeworkNumber -match '^\d{2}$') {
    $nn = $HomeworkNumber
} else {
    throw "Invalid homework number '$HomeworkNumber'. Provide a two-digit number such as '01' or '02'."
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$distDir  = Join-Path $repoRoot 'dist'
New-Item -ItemType Directory -Force -Path $distDir | Out-Null

$zipName = "cse305_hw${nn}_231805033_231805026.zip"
$zipPath = Join-Path $distDir $zipName
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

$excludedTopDirs = @(
    'target',
    '.git',
    '.venv',
    'venv',
    'dist',
    '.idea',
    '.vscode',
    '.settings',
    'node_modules',
    '__pycache__'
)

$excludedFilePatterns = @(
    '*.iml',
    '*.ipr',
    '*.iws',
    '*.mv.db',
    '*.trace.db',
    '*.lock.db',
    '*.log',
    '*.zip',
    '.classpath',
    '.project',
    '.DS_Store',
    'Thumbs.db',
    'Desktop.ini'
)

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    $allFiles = Get-ChildItem -Path $repoRoot -Recurse -Force -File
    $count = 0
    foreach ($file in $allFiles) {
        $relPath = $file.FullName.Substring($repoRoot.Length).TrimStart('\', '/')
        $segments = $relPath -split '[\\/]'

        if ($excludedTopDirs -contains $segments[0]) {
            continue
        }
        if ($segments -contains '__pycache__' -or $segments -contains 'node_modules') {
            continue
        }
        if ($relPath -replace '\\', '/' -match '^data/db(/|$)') {
            continue
        }
        if ($relPath -replace '\\', '/' -in @('.mvn/timing.properties', '.mvn/wrapper/maven-wrapper.jar')) {
            continue
        }

        $skipFile = $false
        foreach ($pattern in $excludedFilePatterns) {
            if ($file.Name -like $pattern) {
                $skipFile = $true
                break
            }
        }
        if ($skipFile) {
            continue
        }

        $entryName = $relPath -replace '\\', '/'
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $zip,
            $file.FullName,
            $entryName,
            [System.IO.Compression.CompressionLevel]::Optimal
        ) | Out-Null
        $count++
    }
} finally {
    $zip.Dispose()
}

Write-Host "Created submission archive: $zipPath ($count files included)"
