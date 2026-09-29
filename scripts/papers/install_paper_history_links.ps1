$ErrorActionPreference = 'Stop'
$root='F:\aicoding\powergrid_benchmark'
$catalog=Get-Content -LiteralPath "$root\docs\migration\paper_organization_20260912\catalog.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$count=0
foreach ($entry in $catalog.history_links) {
 $link=[IO.Path]::GetFullPath((Join-Path $root $entry.link))
 $target=[IO.Path]::GetFullPath((Join-Path $root $entry.target))
 if (!$link.StartsWith($root+'\paper_projects\') -or !$target.StartsWith($root+'\')) {throw 'Invalid boundary'}
 if ($link -notmatch '\\90_History_Links\\[^\\]+$') {throw 'Invalid link placement'}
 $item=Get-Item -LiteralPath $target -Force
 if (!$item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) {throw "Invalid target: $target"}
 if (Test-Path -LiteralPath $link) {
  $existing=Get-Item -LiteralPath $link -Force
  if ($existing.LinkType -ne 'Junction' -or $existing.Target[0] -ne $target) {throw "Collision: $link"}
 } else { New-Item -ItemType Junction -Path $link -Target $target | Out-Null }
 $count++
}
Write-Output "Verified $count permanent history directory entrances. No target files changed."
