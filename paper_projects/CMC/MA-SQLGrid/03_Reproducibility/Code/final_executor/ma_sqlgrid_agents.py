"""Deterministic coordination core for the MA-SQLGrid original-title rebuild.

This module deliberately contains no model client and no gold-SQL access.  A
caller supplies candidate SQL strings and, optionally, reference-free execution
evidence.  The module turns those inputs into an append-only, auditable decision
trace that can be used in a prospectively frozen experiment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import re
from typing import Any, Callable, Iterable, Mapping, Sequence


_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_FORBIDDEN_SQL = re.compile(
    r"\b(?:alter|attach|create|delete|detach|drop|insert|pragma|replace|update|vacuum)\b",
    re.IGNORECASE,
)
_AGGREGATIONS = {
    "average": "AVG",
    "avg": "AVG",
    "count": "COUNT",
    "how many": "COUNT",
    "maximum": "MAX",
    "minimum": "MIN",
    "sum": "SUM",
    "total": "SUM",
}


def canonical_sql(sql: str) -> str:
    """Return a stable comparison form without changing SQL semantics."""

    return re.sub(r"\s+", " ", sql.strip()).rstrip(";").strip() + ";"


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_RE.findall(text)}


@dataclass(frozen=True)
class QueryIntent:
    question_id: str
    question: str
    aggregations: tuple[str, ...]
    order_required: bool
    limit: int | None
    lexical_tokens: tuple[str, ...]


@dataclass(frozen=True)
class SchemaGrounding:
    selected_tables: tuple[str, ...]
    selected_columns: tuple[str, ...]
    join_edges: tuple[tuple[str, str], ...]
    unmatched_tokens: tuple[str, ...]


@dataclass(frozen=True)
class SQLCandidate:
    candidate_id: str
    sql: str
    source: str
    ordinal: int


@dataclass(frozen=True)
class ValidationEvidence:
    candidate_id: str
    safe: bool
    single_statement: bool
    executable: bool
    shape_ok: bool
    order_ok: bool
    value_hits: int
    error: str | None = None
    result_hash: str | None = None


@dataclass(frozen=True)
class CounterfactualEvidence:
    candidate_id: str
    evaluated_states: int
    passed_states: int
    failed_states: tuple[str, ...]
    coverage_complete: bool

    @property
    def pass_rate(self) -> float | None:
        if self.evaluated_states == 0:
            return None
        return self.passed_states / self.evaluated_states


@dataclass(frozen=True)
class AdjudicationScore:
    candidate_id: str
    eligible: bool
    validation_points: int
    counterfactual_passes: int
    counterfactual_total: int
    counterfactual_coverage_complete: bool
    ordinal: int

    @property
    def sort_key(self) -> tuple[int, int, int, int, int]:
        # Ratio comparison is implemented without floating point in Adjudicator.
        return (
            int(self.eligible),
            self.validation_points,
            self.counterfactual_passes,
            -self.counterfactual_total,
            -self.ordinal,
        )


@dataclass(frozen=True)
class Decision:
    selected_candidate_id: str | None
    selected_sql: str | None
    status: str
    rationale: str
    scores: tuple[AdjudicationScore, ...]


@dataclass(frozen=True)
class BlackboardMessage:
    sequence: int
    role: str
    kind: str
    payload: Mapping[str, Any]


@dataclass
class Blackboard:
    """Append-only trace shared by the deterministic agent roles."""

    question_id: str
    _messages: list[BlackboardMessage] = field(default_factory=list, repr=False)
    _sealed: bool = field(default=False, repr=False)

    @property
    def messages(self) -> tuple[BlackboardMessage, ...]:
        return tuple(self._messages)

    def post(self, role: str, kind: str, payload: Mapping[str, Any]) -> None:
        if self._sealed:
            raise RuntimeError("blackboard is sealed")
        self._messages.append(
            BlackboardMessage(
                sequence=len(self._messages),
                role=role,
                kind=kind,
                payload=dict(payload),
            )
        )

    def seal(self) -> None:
        self._sealed = True

    def audit_digest(self) -> str:
        body = {
            "question_id": self.question_id,
            "messages": [asdict(message) for message in self._messages],
            "sealed": self._sealed,
        }
        canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class QueryAnalyst:
    role = "Query Analyst"

    def analyze(self, question_id: str, question: str) -> QueryIntent:
        lowered = question.lower()
        aggregations = tuple(
            sorted({operator for phrase, operator in _AGGREGATIONS.items() if phrase in lowered})
        )
        order_required = any(term in lowered for term in ("highest", "lowest", "top ", "most ", "least ", "order"))
        limit_match = re.search(r"\b(?:top|first)\s+(\d+)\b", lowered)
        limit = int(limit_match.group(1)) if limit_match else (1 if any(term in lowered for term in ("highest", "lowest", "most ", "least ")) else None)
        return QueryIntent(
            question_id=question_id,
            question=question,
            aggregations=aggregations,
            order_required=order_required,
            limit=limit,
            lexical_tokens=tuple(sorted(_tokens(question))),
        )


class SchemaCartographer:
    role = "Schema Cartographer"

    def __init__(self, max_tables: int = 6) -> None:
        if max_tables < 1:
            raise ValueError("max_tables must be positive")
        self.max_tables = max_tables

    def ground(
        self,
        intent: QueryIntent,
        schema: Mapping[str, Sequence[str]],
        foreign_keys: Sequence[tuple[str, str]] = (),
    ) -> SchemaGrounding:
        question_tokens = set(intent.lexical_tokens)
        scored: list[tuple[int, str]] = []
        matched_tokens: set[str] = set()
        for table, columns in schema.items():
            table_tokens = _tokens(table)
            column_tokens = set().union(*(_tokens(column) for column in columns)) if columns else set()
            overlap = question_tokens & (table_tokens | column_tokens)
            if overlap:
                matched_tokens.update(overlap)
                scored.append((len(overlap), table))
        selected = [table for _, table in sorted(scored, key=lambda item: (-item[0], item[1]))[: self.max_tables]]
        if not selected and schema:
            selected = [sorted(schema)[0]]
        selected_set = set(selected)
        joins = tuple(sorted(edge for edge in foreign_keys if edge[0].split(".", 1)[0] in selected_set and edge[1].split(".", 1)[0] in selected_set))
        columns = tuple(
            sorted(
                f"{table}.{column}"
                for table in selected
                for column in schema.get(table, ())
                if _tokens(column) & question_tokens
            )
        )
        return SchemaGrounding(
            selected_tables=tuple(selected),
            selected_columns=columns,
            join_edges=joins,
            unmatched_tokens=tuple(sorted(question_tokens - matched_tokens)),
        )


class SQLSynthesizer:
    """Packages externally produced candidates; it never calls a model."""

    role = "SQL Synthesizer"

    def package(self, sql_strings: Iterable[str], source: str = "external_candidate_provider") -> tuple[SQLCandidate, ...]:
        candidates: list[SQLCandidate] = []
        seen: set[str] = set()
        for sql in sql_strings:
            if not isinstance(sql, str) or not sql.strip():
                continue
            normalized = canonical_sql(sql)
            if normalized in seen:
                continue
            seen.add(normalized)
            candidates.append(
                SQLCandidate(
                    candidate_id=f"C{len(candidates):03d}",
                    sql=normalized,
                    source=source,
                    ordinal=len(candidates),
                )
            )
        if not candidates:
            raise ValueError("at least one non-empty SQL candidate is required")
        return tuple(candidates)


Executor = Callable[[str], Mapping[str, Any]]


class Validator:
    role = "Execution and Safety Validator"

    def validate(self, candidate: SQLCandidate, executor: Executor | None = None) -> ValidationEvidence:
        sql = candidate.sql.strip()
        without_terminal = sql[:-1] if sql.endswith(";") else sql
        single_statement = bool(without_terminal.strip()) and ";" not in without_terminal
        no_comments = "--" not in sql and "/*" not in sql and "*/" not in sql
        read_only_lead = bool(re.match(r"^\s*(?:select|with)\b", sql, re.IGNORECASE))
        safe = bool(single_statement and no_comments and read_only_lead and not _FORBIDDEN_SQL.search(sql))
        if not safe:
            return ValidationEvidence(
                candidate_id=candidate.candidate_id,
                safe=False,
                single_statement=single_statement,
                executable=False,
                shape_ok=False,
                order_ok=False,
                value_hits=0,
                error="read-only single-statement contract rejected candidate",
            )
        if executor is None:
            return ValidationEvidence(
                candidate_id=candidate.candidate_id,
                safe=True,
                single_statement=True,
                executable=False,
                shape_ok=False,
                order_ok=False,
                value_hits=0,
                error="execution evidence unavailable",
            )
        try:
            evidence = dict(executor(sql))
        except Exception as exc:  # evidence must retain failure instead of retrying
            return ValidationEvidence(
                candidate_id=candidate.candidate_id,
                safe=True,
                single_statement=True,
                executable=False,
                shape_ok=False,
                order_ok=False,
                value_hits=0,
                error=f"{type(exc).__name__}: {exc}",
            )
        return ValidationEvidence(
            candidate_id=candidate.candidate_id,
            safe=True,
            single_statement=True,
            executable=bool(evidence.get("executable", evidence.get("ok", False))),
            shape_ok=bool(evidence.get("shape_ok", False)),
            order_ok=bool(evidence.get("order_ok", False)),
            value_hits=max(0, int(evidence.get("value_hits", 0))),
            error=evidence.get("error"),
            result_hash=evidence.get("result_hash"),
        )


class CounterfactualCritic:
    role = "Counterfactual Critic"

    def review(
        self,
        candidate: SQLCandidate,
        state_results: Sequence[Mapping[str, Any]],
        expected_state_ids: Sequence[str] = (),
    ) -> CounterfactualEvidence:
        passed = 0
        failed: list[str] = []
        observed: set[str] = set()
        for index, result in enumerate(state_results):
            state_id = str(result.get("state_id", f"state_{index}"))
            if state_id in observed:
                raise ValueError(f"duplicate counterfactual state: {state_id}")
            observed.add(state_id)
            if bool(result.get("executable", result.get("ok", False))) and bool(result.get("equivalent", False)):
                passed += 1
            else:
                failed.append(state_id)
        expected = set(expected_state_ids)
        return CounterfactualEvidence(
            candidate_id=candidate.candidate_id,
            evaluated_states=len(state_results),
            passed_states=passed,
            failed_states=tuple(sorted(failed)),
            coverage_complete=bool(expected) and observed == expected,
        )


class Adjudicator:
    """Reference-free deterministic adjudication with explicit tie breaking."""

    role = "Adjudicator"

    @staticmethod
    def _validation_points(item: ValidationEvidence) -> int:
        return (
            40 * int(item.safe)
            + 40 * int(item.executable)
            + 10 * int(item.shape_ok)
            + 5 * int(item.order_ok)
            + min(item.value_hits, 5)
        )

    def decide(
        self,
        candidates: Sequence[SQLCandidate],
        validations: Mapping[str, ValidationEvidence],
        counterfactuals: Mapping[str, CounterfactualEvidence],
        *,
        require_counterfactual: bool = False,
        expected_state_count: int = 0,
        minimum_counterfactual_passes: int | None = None,
    ) -> Decision:
        if require_counterfactual and expected_state_count < 1:
            raise ValueError("expected_state_count must be positive when counterfactual evidence is required")
        if minimum_counterfactual_passes is None:
            minimum_counterfactual_passes = expected_state_count if require_counterfactual else 0
        if not 0 <= minimum_counterfactual_passes <= expected_state_count:
            raise ValueError("minimum_counterfactual_passes must be within the expected state count")
        scores: list[AdjudicationScore] = []
        for candidate in candidates:
            validation = validations[candidate.candidate_id]
            cf = counterfactuals.get(
                candidate.candidate_id,
                CounterfactualEvidence(candidate.candidate_id, 0, 0, (), False),
            )
            scores.append(
                AdjudicationScore(
                    candidate_id=candidate.candidate_id,
                    eligible=(
                        validation.safe
                        and validation.executable
                        and (
                            not require_counterfactual
                            or (
                                cf.coverage_complete
                                and cf.evaluated_states == expected_state_count
                                and cf.passed_states >= minimum_counterfactual_passes
                            )
                        )
                    ),
                    validation_points=self._validation_points(validation),
                    counterfactual_passes=cf.passed_states,
                    counterfactual_total=cf.evaluated_states,
                    counterfactual_coverage_complete=cf.coverage_complete,
                    ordinal=candidate.ordinal,
                )
            )
        eligible = [score for score in scores if score.eligible]
        if not eligible:
            rationale = (
                "no candidate had complete required counterfactual coverage and the frozen pass threshold"
                if require_counterfactual
                else "no safe executable candidate"
            )
            return Decision(None, None, "abstain", rationale, tuple(scores))

        def key(score: AdjudicationScore) -> tuple[int, int, int, int]:
            # Complete counterfactual success is used only when evidence exists.
            cf_scaled = (
                score.counterfactual_passes * 1_000_000 // score.counterfactual_total
                if score.counterfactual_total
                else -1
            )
            return (score.validation_points, cf_scaled, score.counterfactual_total, -score.ordinal)

        winner = max(eligible, key=key)
        selected = next(candidate for candidate in candidates if candidate.candidate_id == winner.candidate_id)
        return Decision(
            selected_candidate_id=selected.candidate_id,
            selected_sql=selected.sql,
            status="selected",
            rationale=(
                "highest deterministic validation score, then counterfactual pass rate, "
                "then evaluated-state coverage, then original candidate order"
            ),
            scores=tuple(scores),
        )


class MASQLGridCoordinator:
    """Runs the six roles and records every handoff on one blackboard."""

    def __init__(self, max_tables: int = 6) -> None:
        self.query_analyst = QueryAnalyst()
        self.schema_cartographer = SchemaCartographer(max_tables=max_tables)
        self.sql_synthesizer = SQLSynthesizer()
        self.validator = Validator()
        self.counterfactual_critic = CounterfactualCritic()
        self.adjudicator = Adjudicator()

    def run(
        self,
        *,
        question_id: str,
        question: str,
        schema: Mapping[str, Sequence[str]],
        candidate_sql: Sequence[str],
        executor: Executor | None,
        counterfactual_results: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
        expected_state_ids: Sequence[str] = (),
        require_counterfactual: bool = False,
        minimum_counterfactual_passes: int | None = None,
        foreign_keys: Sequence[tuple[str, str]] = (),
        candidate_source: str = "external_candidate_provider",
    ) -> tuple[Decision, Blackboard]:
        board = Blackboard(question_id=question_id)
        intent = self.query_analyst.analyze(question_id, question)
        board.post(self.query_analyst.role, "query_intent", asdict(intent))
        grounding = self.schema_cartographer.ground(intent, schema, foreign_keys)
        board.post(self.schema_cartographer.role, "schema_grounding", asdict(grounding))
        candidates = self.sql_synthesizer.package(candidate_sql, source=candidate_source)
        board.post(self.sql_synthesizer.role, "sql_candidates", {"candidates": [asdict(item) for item in candidates]})

        validations: dict[str, ValidationEvidence] = {}
        counterfactuals: dict[str, CounterfactualEvidence] = {}
        supplied_cf = counterfactual_results or {}
        for candidate in candidates:
            validation = self.validator.validate(candidate, executor)
            validations[candidate.candidate_id] = validation
            board.post(self.validator.role, "validation_evidence", asdict(validation))
            state_rows = supplied_cf.get(candidate.candidate_id, ())
            cf = self.counterfactual_critic.review(candidate, state_rows, expected_state_ids)
            counterfactuals[candidate.candidate_id] = cf
            board.post(self.counterfactual_critic.role, "counterfactual_evidence", asdict(cf))

        decision = self.adjudicator.decide(
            candidates,
            validations,
            counterfactuals,
            require_counterfactual=require_counterfactual,
            expected_state_count=len(expected_state_ids),
            minimum_counterfactual_passes=minimum_counterfactual_passes,
        )
        board.post(self.adjudicator.role, "decision", asdict(decision))
        board.seal()
        return decision, board
