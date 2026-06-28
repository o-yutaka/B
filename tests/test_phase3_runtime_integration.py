import unittest

from adapters import ExplorerAdapter
from contracts import DecisionPacket, EvidencePacket, ExecutionPacket
from events import EventPublisher, EventType, SubscriptionRegistry
from runtime import Dispatcher, PacketRouter, RuntimeLifecycle


class PacketRouterTest(unittest.TestCase):
    def test_routes_known_packets_without_inspecting_business_logic(self):
        dispatcher = Dispatcher()
        router = PacketRouter(dispatcher)
        packet = DecisionPacket(decision_id="d-1", intent="i", reality="r")

        envelope = router.route(packet)

        self.assertEqual(envelope.event_type, EventType.DECISION_CREATED.value)
        self.assertIs(envelope.payload, packet)
        self.assertEqual(dispatcher.published()[-1], envelope)

    def test_routes_evidence_and_execution_packets(self):
        dispatcher = Dispatcher()
        router = PacketRouter(dispatcher)

        self.assertEqual(router.route(EvidencePacket(source="s", trust_score=1.0)).event_type, EventType.EVIDENCE_CREATED.value)
        self.assertEqual(router.route(ExecutionPacket(execution_id="e", decision_id="d", action="a")).event_type, EventType.EXECUTION_STARTED.value)


class DispatcherPublicationTest(unittest.TestCase):
    def test_subscribe_and_publish_event(self):
        dispatcher = Dispatcher()
        received = []
        SubscriptionRegistry(dispatcher).subscribe(EventType.FEEDBACK_RECEIVED.value, received.append)

        envelope = EventPublisher(dispatcher).publish(EventType.FEEDBACK_RECEIVED.value, {"ok": True})

        self.assertEqual(received, [envelope])
        self.assertEqual(dispatcher.published(), (envelope,))


class FakeExplorer:
    def __init__(self):
        self.calls = []
    def initialize(self, config=None):
        self.calls.append(("initialize", config))
    def register(self, runtime, event_bus):
        self.calls.append(("register", runtime, event_bus))
    def search(self, intent, reality, constraints=()):
        self.calls.append(("search", intent, reality, constraints))
        return ("evidence",)
    def health(self):
        return {"status": "ok"}
    def shutdown(self):
        self.calls.append(("shutdown",))


class LifecycleAndAdapterTest(unittest.TestCase):
    def test_lifecycle_registers_adapter_and_adapter_publishes_result(self):
        dispatcher = Dispatcher()
        explorer = FakeExplorer()
        adapter = ExplorerAdapter(explorer)
        lifecycle = RuntimeLifecycle(dispatcher)

        lifecycle.initialize([adapter], {"phase": "3"})
        packet = DecisionPacket(decision_id="d-2", intent="intent", reality="reality")
        EventPublisher(dispatcher).publish(EventType.DECISION_CREATED.value, packet)

        event_types = [event.event_type for event in dispatcher.published()]
        self.assertIn(EventType.RUNTIME_INITIALIZED.value, event_types)
        self.assertIn(EventType.EVIDENCE_CREATED.value, event_types)
        self.assertEqual(explorer.calls[0], ("initialize", {"phase": "3"}))
        self.assertEqual(explorer.calls[-1], ("search", "intent", "reality", ()))

        lifecycle.shutdown()
        self.assertEqual(dispatcher.published()[-1].event_type, EventType.RUNTIME_SHUTDOWN.value)


if __name__ == "__main__":
    unittest.main()
