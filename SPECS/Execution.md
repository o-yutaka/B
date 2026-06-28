# Execution Specification

## Purpose

Execution modules perform approved actions and publish completion evidence.

## Event Boundary

- Subscribes: `execution.requested`
- Publishes: `execution.started`, `execution.finished`, `execution.failed`

## Constraint

Execution must only act on approved decisions and must emit replayable feedback.
