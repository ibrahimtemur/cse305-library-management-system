# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: PowerShell wrapper for generating leak-free, print-ready PDFs from Markdown documents.

[CmdletBinding()]
param(
    [string]$InputPath = "docs/01-proposal/HW01_Problem_Solution_DomainModel.md",
    [string]$OutputPath = "docs/01-proposal/HW01_Problem_Solution_DomainModel.pdf",
    [string]$RootOutputPath = "HW01_Problem_Solution_DomainModel.pdf"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "export-pdf.py"

python $pythonScript --input $InputPath --output $OutputPath --root-output $RootOutputPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "PDF export failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
