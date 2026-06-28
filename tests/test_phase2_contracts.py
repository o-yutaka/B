import unittest
from dataclasses import FrozenInstanceError

from contracts import DecisionPacket, EvidencePacket
from interfaces import IExplorer, IGovernance, IKernel, IMemory, IReasoner, IWorldModel
from ontology import CONCEPTS, get_concept
from registry import CapabilityDescriptor, CapabilityRegistry, ServiceLocator


class DecisionPacketTest(unittest.TestCase):
    def test_decision_packet_is_immutable_and_validates_scores(self):
        packet = DecisionPacket(
            decision_id="d-1",
            intent="intent",
            reality={"state": "known"},
            confidence=0.5,
            risk=0.25,
            metadata={"trace": "t-1"},
        )
        self.assertEqual(packet.decision_id, "d-1")
        with self.assertRaises(FrozenInstanceError):
            packet.verdict = "approved"
        with self.assertRaises(ValueError):
            DecisionPacket(decision_id="d-2", intent="i", reality="r", confidence=1.1)


class EvidencePacketTest(unittest.TestCase):
    def test_evidence_packet_validates_source_and_scores(self):
        packet = EvidencePacket(source="sensor", trust_score=0.8, confidence=0.7)
        self.assertEqual(packet.validation_state, "unvalidated")
        with self.assertRaises(ValueError):
            EvidencePacket(source="", trust_score=0.1)
        with self.assertRaises(ValueError):
            EvidencePacket(source="sensor", trust_score=-0.1)


class InterfaceContractTest(unittest.TestCase):
    def test_interfaces_are_abstract(self):
        for interface in (IExplorer, IReasoner, IKernel, IWorldModel, IMemory, IGovernance):
            self.assertTrue(interface.__abstractmethods__)
            with self.assertRaises(TypeError):
                interface()


class CapabilityRegistryTest(unittest.TestCase):
    def test_register_lookup_and_metadata(self):
        registry = CapabilityRegistry()
        descriptor = CapabilityDescriptor(
            name="observe.reality",
            provider="world_model",
            metadata={"event": "world_model.observe"},
        )
        registry.register(descriptor)
        self.assertIs(registry.lookup("observe.reality"), descriptor)
        self.assertEqual(registry.metadata("observe.reality")["event"], "world_model.observe")
        with self.assertRaises(ValueError):
            registry.register(descriptor)

    def test_service_locator_has_no_global_state(self):
        first = ServiceLocator()
        second = ServiceLocator()
        first.register("bus", object())
        self.assertTrue(first.has("bus"))
        self.assertFalse(second.has("bus"))


class OntologyTest(unittest.TestCase):
    def test_required_concepts_exist_with_contract_fields(self):
        required = {
            "Intent", "Decision", "Reality", "Truth", "Evidence", "Constraint", "Capability",
            "Confidence", "Risk", "Debt", "Verdict", "Observation", "Prediction", "Simulation",
            "Feedback", "Memory", "Compression",
        }
        self.assertEqual(set(CONCEPTS), required)
        for name in required:
            concept = get_concept(name)
            self.assertTrue(concept.definition)
            self.assertTrue(concept.purpose)
            self.assertTrue(concept.producer)
            self.assertTrue(concept.consumer)


if __name__ == "__main__":
    unittest.main()
