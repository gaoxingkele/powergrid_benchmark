# MA-SQLGrid Original-Title Rebuild: Coordination Core

This directory is an additive, pre-experiment workspace for the manuscript titled
**“MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases.”**
It does not modify or supersede any frozen run.

## Implemented boundary

`ma_sqlgrid_agents.py` provides six explicit roles:

1. Query Analyst: produces a structured, question-only intent record.
2. Schema Cartographer: produces a deterministic lexical schema grounding.
3. SQL Synthesizer: packages and deduplicates candidates supplied by an external
   generator. It contains no API client.
4. Execution and Safety Validator: enforces the read-only single-statement
   contract and records caller-supplied execution evidence.
5. Counterfactual Critic: records pass/fail evidence from named database states;
   missing states remain unknown rather than being counted as passes.
6. Adjudicator: selects by a frozen deterministic rule and abstains when no safe,
   executable candidate exists.

The append-only blackboard records every handoff and emits a canonical SHA-256
digest. Gold SQL, gold results, and answer labels are not accepted by the public
coordinator interface and are not used for selection.

## Run the offline unit tests

From this directory:

```powershell
python -m unittest discover -s tests -v
```

The tests use synthetic executor evidence. They do not call an LLM, access a
frozen result directory, or run a generation experiment.

## Scientific status

This is a **testable coordination skeleton**, not evidence that multi-agent
coordination improves accuracy. The claims enabled by this directory are limited
to implementation properties verified by its tests. Performance claims require
a separately approved, prospectively frozen experiment under
`FREEZE_PROTOCOL_DRAFT.md`.

## Retrospective read-only replay

`replay_diagnostic.py` verifies the SHA-256 values of the frozen Qwen and
Granite prediction ledgers and the formal-v5 atomic-score ledger before reading
them. It pools the already generated SQL strings per question, runs the new
Validator, invokes the Counterfactual Critic in fail-closed mode, and permits the
Adjudicator to act only when at least two distinct candidates are safe and have
consistent frozen T0 execution evidence.

```powershell
python -B replay_diagnostic.py
```

The generated `retrospective_diagnostic/` directory contains a 180-row audit
ledger, coverage statistics and a hash manifest. These artifacts are always
labelled **retrospective offline coordination diagnostic**. They are not new
model calls, a new multi-agent generation result, an accuracy estimate or
evidence of a counterfactual gain.

