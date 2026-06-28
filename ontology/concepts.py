"""Canonical decision-language concepts for BLACK v1 Phase 2."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Concept:
    """Immutable ontology concept definition used across BLACK contracts."""

    name: str
    definition: str
    purpose: str
    producer: str
    consumer: str

    def as_metadata(self) -> Mapping[str, str]:
        return MappingProxyType({
            "name": self.name,
            "definition": self.definition,
            "purpose": self.purpose,
            "producer": self.producer,
            "consumer": self.consumer,
        })


CONCEPTS: Mapping[str, Concept] = MappingProxyType({
    "Intent": Concept("Intent", "A declared objective or desired state that initiates a decision cycle.", "Preserve why a decision exists before actions are considered.", "Goal generation, users, task intelligence", "Reasoner, kernel, governance"),
    "Decision": Concept("Decision", "A selected or rejected course of action under stated evidence, reality, constraints, confidence, and risk.", "Make choices auditable and transportable between subsystems.", "Kernel", "Execution, memory, governance"),
    "Reality": Concept("Reality", "The bounded representation of current operating conditions relevant to an intent.", "Anchor decisions to observed context instead of assumptions.", "World model, explorer, event bus", "Reasoner, kernel, governance"),
    "Truth": Concept("Truth", "A claim state accepted within a declared validation boundary and provenance chain.", "Separate validated claims from raw observations or predictions.", "Governance, evidence validation", "Reasoner, kernel, memory"),
    "Evidence": Concept("Evidence", "A sourced item that supports, weakens, or contextualizes a claim or candidate action.", "Give every decision an inspectable basis.", "Explorer, world model, memory, governance", "Reasoner, kernel, decision packet"),
    "Constraint": Concept("Constraint", "A boundary that limits acceptable actions, resources, timing, policy, or risk.", "Prevent decisions from violating known limits.", "Governance, runtime, user, environment", "Reasoner, kernel, execution"),
    "Capability": Concept("Capability", "A named ability a subsystem or tool can provide with metadata and constraints.", "Allow planning without direct subsystem coupling.", "Capability registry, modules", "Kernel, reasoner, service locator"),
    "Confidence": Concept("Confidence", "A normalized degree of support for evidence, predictions, or decisions.", "Expose uncertainty explicitly.", "Evidence validation, reasoner, world model", "Kernel, governance, memory"),
    "Risk": Concept("Risk", "A typed estimate of downside exposure associated with an action or decision.", "Make unsafe or costly choices visible before execution.", "Governance, reasoner, world model", "Kernel, execution, memory"),
    "Debt": Concept("Debt", "A deferred cost, unresolved uncertainty, or compromise created by a decision.", "Track long-term obligations introduced by short-term choices.", "Kernel, governance, memory", "Goal generation, reasoner, governance"),
    "Verdict": Concept("Verdict", "The governance-compatible decision state such as approved, rejected, deferred, or needs evidence.", "Provide a canonical handoff state for downstream systems.", "Kernel, governance", "Execution, memory, runtime"),
    "Observation": Concept("Observation", "A recorded signal from the environment or a subsystem at a known time.", "Feed reality construction and evidence generation.", "Event bus, world model, explorer", "Evidence, memory, reasoner"),
    "Prediction": Concept("Prediction", "A stated expectation about a future state with confidence and provenance.", "Make foresight inspectable without treating it as fact.", "World model, reasoner", "Simulation, kernel, governance"),
    "Simulation": Concept("Simulation", "A bounded projection of possible outcomes for candidate actions.", "Represent consequence estimates without executing actions.", "World model, reasoner", "Kernel, governance, memory"),
    "Feedback": Concept("Feedback", "A post-decision signal describing observed execution results or external response.", "Close the decision loop for learning and audit.", "Execution, event bus, users", "Memory, goal generation, governance"),
    "Memory": Concept("Memory", "Durable retained information about observations, evidence, decisions, feedback, and compressed history.", "Provide continuity across decision cycles.", "Memory subsystem", "Explorer, reasoner, kernel, governance"),
    "Compression": Concept("Compression", "A controlled transformation that reduces stored information while preserving declared decision value.", "Keep memory usable at scale without hiding provenance.", "Memory, compression subsystem", "Reasoner, governance, explorer"),
})


def get_concept(name: str) -> Concept:
    """Return a canonical concept by exact name."""
    return CONCEPTS[name]
