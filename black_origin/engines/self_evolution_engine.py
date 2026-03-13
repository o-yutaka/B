class SelfEvolutionEngine:
    def evolve(self, research_memory, agent_outputs):
        avg_confidence = sum(item["confidence"] for item in agent_outputs) / max(1, len(agent_outputs))
        improvement = {
            "focus": "agent_strategy",
            "proposal": "Increase analysis_agent weight when volatility is elevated",
            "score": round(avg_confidence, 2),
        }
        research_memory["improvements"].append(improvement)
        research_memory["improvements"] = research_memory["improvements"][-20:]
        return research_memory
