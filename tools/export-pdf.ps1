# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: PowerShell wrapper for generating leak-free, print-ready PDFs from Markdown documents with configurable input, docs output, and optional root output paths.

[CmdletBinding()]
param(
    [Alias("InputPath")]
    [string]$Input = "docs/01-proposal/HW01_Problem_Solution_DomainModel.md",

    [Alias("OutputPath", "Output")]
    [string]$DocsOutput = "docs/01-proposal/HW01_Problem_Solution_DomainModel.pdf",

    [Alias("RootOutputPath")]
    [string]$RootOutput = ""
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "export-pdf.py"

$cmdArgs = @($pythonScript, "--input", $Input, "--docs-output", $DocsOutput)
if (-not [string]::IsNullOrWhiteSpace($RootOutput)) {
    $cmdArgs += @("--root-output", $RootOutput)
} elseif ($Input -eq "docs/01-proposal/HW01_Problem_Solution_DomainModel.md" -and -not $PSBoundParameters.ContainsKey("RootOutput")) {
    $cmdArgs += @("--root-output", "HW01_Problem_Solution_DomainModel.pdf")
}

python @cmdArgs

if ($LASTEXITCODE -ne 0) {
    Write-Error "PDF export failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
