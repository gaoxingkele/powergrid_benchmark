# Logs

`run.log` is created by the single approved execution and contains timestamped
progress, preflight checks, per-run completion lines, and final output paths.
The script does not retry failed model runs. A completed manifest prevents a
second execution in this namespace.
