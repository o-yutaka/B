class AgentSystem:
    AGENTS = [
        "collector_agent",
        "analysis_agent",
        "simulation_agent",
        "strategy_agent",
        "research_agent",
    ]

    def run(self, prediction):
        outputs = []
        for name in self.AGENTS:
            outputs.append(
                {
                    "agent": name,
                    "action": f"{name} processed scenario {prediction['future_scenario']}",
                    "confidence": round(0.55 + prediction["risk_signal"] * 0.35, 2),
                }
            )
        return outputs
