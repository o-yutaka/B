class CausalGraphEngine:
    RULES = [
        ("energy supply", "inflation", "temporal_correlation", 0.61),
        ("inflation", "interest rates", "event_analysis", 0.74),
        ("interest rates", "economic growth", "bayesian_inference", 0.58),
    ]

    def infer(self, causal_state, cycle: int):
        source, target, method, confidence = self.RULES[(cycle - 1) % len(self.RULES)]
        link = {
            "source": source,
            "target": target,
            "method": method,
            "confidence": round(confidence + (cycle % 5) * 0.01, 2),
        }
        if link not in causal_state["links"]:
            causal_state["links"].append(link)
        causal_state["evidence"].append(
            {
                "cycle": cycle,
                "observation": f"{source} signal shifted before {target}",
                "method": method,
            }
        )
        causal_state["evidence"] = causal_state["evidence"][-25:]
        return causal_state
