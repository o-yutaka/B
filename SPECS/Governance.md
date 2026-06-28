# Governance Specification

## Purpose

Governance applies Constitution and evidence rules to proposed changes and decisions.

## Event Boundary

- Subscribes: `governance.review.requested`
- Publishes: `governance.review.completed`

## Constraint

Governance protects decision integrity without bypassing RuntimeEngine or EventBus.
