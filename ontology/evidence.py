"""Canonical evidence ontology exports."""
from .concepts import Concept, get_concept

EVIDENCE_CONCEPT: Concept = get_concept("Evidence")

__all__ = ["EVIDENCE_CONCEPT"]
