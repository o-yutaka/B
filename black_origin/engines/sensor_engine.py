class SensorEngine:
    def synthesize_sensors(self, event_stream):
        topic_counts = {}
        for event in event_stream:
            topic_counts[event["topic"]] = topic_counts.get(event["topic"], 0) + 1
        return [{"topic": topic, "intensity": count} for topic, count in topic_counts.items()]
