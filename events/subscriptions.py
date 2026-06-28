"""Subscription helpers for canonical runtime events."""
from runtime.dispatcher import Dispatcher, Subscriber

class SubscriptionRegistry:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher

    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        self._dispatcher.subscribe(event_type, subscriber)
