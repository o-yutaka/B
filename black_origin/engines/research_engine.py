class ResearchEngine:
    def run(self, research_memory, world_model, prediction):
        dominant = max(world_model["domains"].items(), key=lambda item: item[1]["signal"])
        hypothesis = f"When {dominant[0]} signal increases, {prediction['trend_forecast']} market behavior follows"
        insight = {
            "cycle": prediction["cycle"],
            "pattern": f"dominant_domain={dominant[0]}",
            "hypothesis": hypothesis,
            "result": f"risk={prediction['risk_signal']}",
        }
        research_memory["insights"].append(insight)
        research_memory["insights"] = research_memory["insights"][-40:]
        return research_memory
