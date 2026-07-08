# Problem

## Research Question

Can a transparent role-aware ranker recover causal-role evidence sentence IDs from power-grid reliability report excerpts better than generic lexical or semantic retrieval baselines?

## Benchmark Task

NERC report sentences plus a causal role/question are mapped to evidence sentence IDs.

## Inputs

- Report excerpt sentences.
- Causal role: trigger event, root cause, propagation or response, impact, or mitigation.
- Role-conditioned question.

## Outputs

Ranked evidence sentence IDs, evaluated primarily by evidence precision, recall, and F1.
