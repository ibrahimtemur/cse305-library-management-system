# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Sets the repository-local Git user.name and user.email for the active team member on this shared computer.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('ibrahim', 'omer', IgnoreCase = $true)]
    [string]$Author
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$gitDir = Join-Path $repoRoot '.git'
if (-not (Test-Path $gitDir)) {
    throw "Git repository is not initialized at '$repoRoot'. Run 'git init' first."
}

$authors = @{
    'ibrahim' = @{
        Name  = 'Ibrahim Temur'
        Email = 'ibrahimtemur847@gmail.com'
        No    = '231805033'
    }
    'omer'    = @{
        Name  = ('Omer Faruk Ku' + [char]0x015F)
        Email = '231805026@stu.adu.edu.tr'
        No    = '231805026'
    }
}

$key = $Author.ToLowerInvariant()
$selected = $authors[$key]

git -C $repoRoot config --local user.name $selected.Name
git -C $repoRoot config --local user.email $selected.Email

$configuredName  = (git -C $repoRoot config --local --get user.name)
$configuredEmail = (git -C $repoRoot config --local --get user.email)

Write-Host "Repository-local Git author set to: $configuredName ($($selected.No)) <$configuredEmail>"
