# Compression Specification

## Purpose

Compression modules reduce memory and evidence traces into durable summaries without losing replayability.

## Event Boundary

- Subscribes: `memory.updated`
- Publishes: `compression.completed`

## Constraint

Compression may reduce size, but not decision integrity.
