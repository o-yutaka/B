"""Canonical capability ontology exports."""
from .concepts import Concept, get_concept

CAPABILITY_CONCEPT: Concept = get_concept("Capability")

__all__ = ["CAPABILITY_CONCEPT"]
