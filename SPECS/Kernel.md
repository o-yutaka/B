# Kernel Specification

## Position in BLACK

The Kernel component evaluates evidence-driven decisions. It is a component of BLACK, not BLACK itself.

## Existing-Architecture Constraint

Changes to this component must preserve the current BLACK ORIGIN intelligence loop unless an accepted ADR explicitly supersedes it. New work must extend the RuntimeEngine and EventBus integration model rather than bypass it.

## Evidence Obligations

Any Kernel change must declare the evidence it consumes, the decision it supports, and the replay record it leaves behind.

## Runtime Integration

A concrete implementation must integrate through the RuntimeEngine and event bus. The expected event boundary for this component is `decision.evaluate` unless a later ADR defines a better contract.

## Decision Integrity Checks

- Does the change improve Decision Quality?
- Does it reduce or explicitly track Decision Debt?
- Can the decision path be replayed from evidence and memory or ledger records?
- Does it keep BLACK as the center rather than optimizing Kernel for its own sake?
