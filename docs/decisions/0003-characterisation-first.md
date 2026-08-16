# ADR 0003: Characterisation before behaviour change

## Status

Accepted

## Context

Matching used Jaccard similarity with non-deterministic story sampling and
several accidental no-ops. A blind rewrite would hide whether upgrades changed
product rules.

## Decision

Extract the matcher into a pure module first and pin it with characterisation
tests. Security issues (cross-user match lookup, listing every waiting room)
are fixed deliberately and recorded in `docs/known-failures.md`.

## Consequences

Algorithm ties still keep the first winner. Empty unions no longer crash.
Story choice remains sampled from the intersection unless a test injects `rng`.
