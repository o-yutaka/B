class WorldModelEngine:
    def update(self, world_model, sensors, causal_links):
        sensor_map = {s["topic"]: s["intensity"] for s in sensors}
        for domain, values in world_model["domains"].items():
            signal = float(sensor_map.get(domain, 0))
            values["signal"] = round((values.get("signal", 0.0) * 0.7) + signal * 0.3, 3)

        if causal_links:
            latest = causal_links[-1]
            world_model["domains"]["economy"]["signal"] = round(
                world_model["domains"]["economy"]["signal"] + latest["confidence"] * 0.05,
                3,
            )
        return world_model
