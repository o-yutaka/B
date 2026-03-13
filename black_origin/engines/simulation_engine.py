class SimulationEngine:
    SCENARIOS = ["economic_shock", "energy_transition", "climate_disruption", "technology_shift"]

    def run(self, world_model, cycle: int):
        scenario = self.SCENARIOS[(cycle - 1) % len(self.SCENARIOS)]
        economy_signal = world_model["domains"]["economy"]["signal"]
        risk = min(1.0, round(0.2 + economy_signal * 0.15 + (cycle % 3) * 0.08, 3))
        return {
            "cycle": cycle,
            "scenario": scenario,
            "risk": risk,
            "summary": f"Scenario {scenario} evaluated with risk score {risk}",
        }
