# Paper Refine Workspace

You are running inside a Paper Refine WebUI workspace.

This directory is an isolated copy of an uploaded LaTeX paper project. Treat files in this directory as the only refinement target. Do not modify files outside this workspace unless the user explicitly asks.

## Harness Context

Paper Refine WebUI provides source file browsing/editing, PDF preview, LaTeX compile, git status/diff/log/commit controls, and this Codex terminal.

The local .git history belongs to this paper refinement workspace only. It starts from the uploaded baseline and is used to track paper changes.

## Working Rules

- Prefer small, section-scoped edits.
- Change LaTeX source, not generated PDF files.
- Do not change citations, equations, labels, numeric results, experimental conclusions, author metadata, acknowledgements, or contribution boundaries without explicit user approval.
- Inspect git diff before summarizing or committing changes.
- Ask before committing unless the user explicitly requested a commit.
- Do not edit Paper Refine WebUI app files or parent repository files from this session.

## Skills

For polishing, de-AI wording, or section-level refinement, use .codex/skills/paper-polish/SKILL.md.
For creating or refining an explicit measurable goal, use .codex/skills/define-goal/SKILL.md.
