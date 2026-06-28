"""Canonical constraint ontology exports."""
from .concepts import Concept, get_concept

CONSTRAINT_CONCEPT: Concept = get_concept("Constraint")

__all__ = ["CONSTRAINT_CONCEPT"]
