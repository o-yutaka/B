"""Canonical reality ontology exports."""
from .concepts import Concept, get_concept

REALITY_CONCEPT: Concept = get_concept("Reality")

__all__ = ["REALITY_CONCEPT"]
