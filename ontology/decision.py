"""Canonical decision ontology exports."""
from .concepts import Concept, get_concept

DECISION_CONCEPT: Concept = get_concept("Decision")

__all__ = ["DECISION_CONCEPT"]
