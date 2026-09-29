param([switch]$Execute)
$ErrorActionPreference = 'Stop'
$root = 'F:\aicoding\powergrid_benchmark'
if (!(Test-Path -LiteralPath "$root\.git" -PathType Container)) { throw 'Unexpected workspace' }
$ids = @(
 @('mintou_p1_dstar_gru_dispatch','GRU-LSR'),
 @('mintou_p2_hygraph_load_forecasting','CSA-LoadNet'),
 @('mintou_p3_samode_distribution_planning','CARS-MODE'),
 @('mintou_p4_shield_resilience_planning','SHIELD-MOEA'),
 @('mintou_p5_trace_moea_feasibility_review','TRACE-MOEA'),
 @('mintou_p6_bilonsga_project_review','BiLo-NSGA')
)
$moves = @()
foreach ($id in $ids) {
 $moves += [pscustomobject]@{source="paper_projects/$($id[0])";target="paper_projects/$($id[1])"}
 $moves += [pscustomobject]@{source="papers/mintou/$($id[0])";target="paper_projects/$($id[1])/ARA"}
}
foreach ($id in @('C2GES','MA-SQLGrid')) {
 $moves += [pscustomobject]@{source="paper_projects/CMC/$id";target="paper_projects/$id/Workspace"}
}
function CheckedPath([string]$relative) {
 $p = [IO.Path]::GetFullPath((Join-Path $root $relative))
 if (!$p.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $p" }
 return $p
}
function Inventory([string]$base) {
 $stack = [Collections.Generic.Stack[string]]::new()
 $stack.Push($base)
 while ($stack.Count) {
  foreach ($entry in Get-ChildItem -LiteralPath $stack.Pop() -Force) {
   if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "Reparse point: $($entry.FullName)" }
   if ($entry.Name -eq '.git') { throw "Nested Git: $($entry.FullName)" }
   if ($entry.PSIsContainer) { $stack.Push($entry.FullName) }
   else { [pscustomobject]@{path=$entry.FullName.Substring($base.Length+1);bytes=$entry.Length;sha256=(Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash} }
  }
 }
}
$preflight = @()
foreach ($move in $moves) {
 $source=CheckedPath $move.source; $target=CheckedPath $move.target
 $item=Get-Item -LiteralPath $source -Force
 if (!$item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) { throw "Source is not a real directory: $source" }
 if (Test-Path -LiteralPath $target) { throw "Destination exists: $target" }
 $records=@(Inventory $source)
 $preflight += [pscustomobject]@{source=$source;target=$target;files=$records}
 [pscustomobject]@{source=$source;target=$target;files=$records.Count} | ConvertTo-Json -Compress
}
if ($preflight.Count -ne 14) { throw 'Expected exactly 14 directories' }
if (!$Execute) { return }
$audit=CheckedPath 'docs/migration/paper_organization_20260912'
if (Test-Path -LiteralPath $audit) { throw 'Audit already exists; do not rerun a completed/partial migration' }
New-Item -ItemType Directory -Path $audit | Out-Null
$preflight | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$audit\before.json" -Encoding UTF8
$completed=@()
foreach ($move in $preflight) {
 # Revalidate immediately in this foreground shell; no recursive operation traverses a link.
 $source=$move.source; $target=$move.target
 if (!$source.StartsWith($root+'\') -or !$target.StartsWith($root+'\')) { throw 'Boundary failure' }
 $current=@(Inventory $source)
 if ((ConvertTo-Json $current -Depth 4 -Compress) -ne (ConvertTo-Json $move.files -Depth 4 -Compress)) { throw "Source changed since preflight: $source" }
 if (Test-Path -LiteralPath $target) { throw "Destination collision: $target" }
 $parent=Split-Path -Parent $target
 if (!(Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent | Out-Null }
 Move-Item -LiteralPath $source -Destination $target
 $after=@(Inventory $target)
 if ((ConvertTo-Json $after -Depth 4 -Compress) -ne (ConvertTo-Json $move.files -Depth 4 -Compress)) { throw "Post-move hash mismatch: $target" }
 # Compatibility links are permanent source entrances, NEVER cleanup-managed directories.
 New-Item -ItemType Junction -Path $source -Target $target | Out-Null
 if ((Get-Item -LiteralPath $source).LinkType -ne 'Junction') { throw 'Compatibility junction failed' }
 $completed += [pscustomobject]@{source=$source;target=$target;files=$after.Count;sha256_verified=$true;compatibility='junction'}
 $completed | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath "$audit\completed.json" -Encoding UTF8
}
Write-Output "VERIFIED $($completed.Count) directories; no source contents edited or deleted."
