$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -3 v2/install.py
} else {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { throw 'Python 3.11+ is required. Install Python and re-run this installer.' }
    & $python.Source v2/install.py
}
