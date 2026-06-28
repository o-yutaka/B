# World Model Specification

## Purpose

World Model modules simulate possible outcomes and maintain environment assumptions for decisions.

## Decision Table

| Input | Output | Event |
| --- | --- | --- |
| Scenario request | Simulation placeholder result | `world_model.simulation.completed` |
| Digital twin update | Model state acknowledgement | `world_model.updated` |

## Constraint

The World Model informs decisions; it must not become the decision authority.
