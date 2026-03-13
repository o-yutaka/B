from datetime import datetime, timezone


class EventEngine:
    def generate_events(self, normalized_entities, cycle: int):
        created = datetime.now(timezone.utc).isoformat()
        events = []
        for index, entity in enumerate(normalized_entities):
            events.append(
                {
                    "id": f"evt-{cycle}-{index}",
                    "type": "discovery_update",
                    "entity": entity["entity"],
                    "topic": entity["topic"],
                    "timestamp": created,
                }
            )
        return events
