# Internal execution logs

- `smoke.log`: preserved failed smoke attempt; packaged `torch.optim` imported
  unavailable `sympy`.
- `smoke2.log`: successful one-seed smoke after switching to the recorded
  eager-mode Adam equations. The frozen scientific settings were unchanged.
- `run.log`: dry-run validation followed by the completed 510-row run.
- `acceptance.log`: failed acceptance attempt with the isolated repository
  `src` path; the checkout lacks the shared `mintou_experiments.py` module.
- `acceptance_attempt3.log`: successful required evidence acceptance run using
  the read-only source workspace for that missing shared regression-test
  import. Matrix, manuscript, and evidence-tree checks still targeted the
  isolated worktree.

The first acceptance attempt (without `PYTHONPATH`) also failed during test
collection before any scientific regression test ran. Its terminal output was
not redirected to a file; it is reported in the executor handoff rather than
reconstructed here.
