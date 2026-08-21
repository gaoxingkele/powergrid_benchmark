$ErrorActionPreference = 'Stop'
$bundleDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $bundleDir 'verify_local_bundle.py')
if ($LASTEXITCODE -ne 0) { throw 'Local reproducibility bundle verification failed.' }
python (Join-Path $bundleDir 'verify_canonical_gzip.py')
if ($LASTEXITCODE -ne 0) { throw 'Canonical gzip payload verification failed.' }
$c2Root = Split-Path -Parent (Split-Path -Parent $bundleDir)
python (Join-Path $c2Root 'exploratory_v3/validate_exploratory_v3.py')
if ($LASTEXITCODE -ne 0) { throw 'Exploratory-v3 validation failed.' }
python (Join-Path $c2Root 'addon_round3/validate_addon.py')
if ($LASTEXITCODE -ne 0) { throw 'Round-3 add-on validation failed.' }
python (Join-Path $c2Root 'bge_expansion_20260806/validate_bge.py')
if ($LASTEXITCODE -ne 0) { throw 'BGE baseline validation failed.' }
