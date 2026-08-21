param(
    [switch]$IncludeDatabases
)

$ErrorActionPreference = 'Stop'

$ProtocolRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$MetadataDir = Join-Path $ProtocolRoot 'official_metadata'
$DownloadDir = Join-Path $ProtocolRoot 'official_downloads'
$DownloadLib = 'D:\aicoding\Lib'

if (-not (Test-Path -LiteralPath $DownloadLib -PathType Container)) {
    throw "Global download library not found: $DownloadLib"
}

New-Item -ItemType Directory -Force -Path $MetadataDir | Out-Null
New-Item -ItemType Directory -Force -Path $DownloadDir | Out-Null
$env:PYTHONPATH = $DownloadLib

function Invoke-OfficialDownload {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Destination,
        [long]$ExpectedBytes = -1,
        [string]$ExpectedSha256
    )

    python -m download_tools $Url $Destination
    if ($LASTEXITCODE -ne 0) {
        throw "Download failed: $Url"
    }

    $Item = Get-Item -LiteralPath $Destination -ErrorAction Stop
    if ($ExpectedBytes -ge 0 -and $Item.Length -ne $ExpectedBytes) {
        throw "Byte-count mismatch for ${Destination}: got $($Item.Length), expected $ExpectedBytes"
    }

    $Hash = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
    if ($ExpectedSha256 -and $Hash -ne $ExpectedSha256.ToLowerInvariant()) {
        throw "SHA-256 mismatch for ${Destination}: got $Hash, expected $ExpectedSha256"
    }

    [pscustomobject]@{
        path = $Item.FullName
        bytes = $Item.Length
        sha256 = $Hash
    }
}

$Results = @()
$Results += Invoke-OfficialDownload `
    -Url 'https://huggingface.co/datasets/birdsql/bird_sql_dev_20251106/resolve/3c11fb193e5439b338e23677fa0aae11e8b85db9/data/dev_20251106-00000-of-00001.json?download=true' `
    -Destination (Join-Path $MetadataDir 'bird_dev_20251106.json') `
    -ExpectedBytes 946793 `
    -ExpectedSha256 'ffd8018378ddb1a8794753e0a31cfc81862ff7318a5184c22f3dc4ce03a03feb'

$Results += Invoke-OfficialDownload `
    -Url 'https://huggingface.co/datasets/birdsql/bird_mini_dev/resolve/f65faf4ae3b638c1fa6df1d3370c8d92c8366301/data/mini_dev_sqlite-00000-of-00001.json?download=true' `
    -Destination (Join-Path $MetadataDir 'bird_mini_dev_sqlite.json') `
    -ExpectedBytes 278513 `
    -ExpectedSha256 '88ceb0710163cae46a256ecea8f0a8c98286599530b60587fda5c3cfe57d45d2'

if ($IncludeDatabases) {
    $Results += Invoke-OfficialDownload `
        -Url 'https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip' `
        -Destination (Join-Path $DownloadDir 'bird_dev.zip') `
        -ExpectedBytes 346207293
}

$Results | Format-Table -AutoSize

if ($IncludeDatabases) {
    Write-Warning 'Do not extract or run a model yet. Copy the printed archive SHA-256 into a reviewed FROZEN_NOT_RUN protocol first.'
} else {
    Write-Output 'Metadata-only acquisition complete. Use -IncludeDatabases only after the draft protocol is approved.'
}
