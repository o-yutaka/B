class PredictionEngine:
    def generate(self, simulation_result, causal_links):
        latest_link = causal_links[-1] if causal_links else None
        trend = "stable"
        if simulation_result["risk"] > 0.6:
            trend = "volatile"
        elif simulation_result["risk"] > 0.35:
            trend = "watch"

        return {
            "cycle": simulation_result["cycle"],
            "trend_forecast": trend,
            "risk_signal": simulation_result["risk"],
            "future_scenario": simulation_result["scenario"],
            "driver": latest_link,
        }
