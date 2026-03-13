class PlanetaryGraphEngine:
    def render_state(self, knowledge_graph, causal_graph, events):
        nodes = [
            {
                "id": entity["name"],
                "group": entity.get("category", "general"),
            }
            for entity in knowledge_graph["entities"]
        ]
        links = [
            {"source": rel["source"], "target": rel["target"], "type": rel["type"]}
            for rel in knowledge_graph["relationships"]
        ]
        causal_links = [
            {"source": link["source"], "target": link["target"], "confidence": link["confidence"]}
            for link in causal_graph["links"]
        ]
        hotspots = [{"label": event["topic"], "event": event["entity"]} for event in events[-10:]]
        return {
            "nodes": nodes,
            "links": links,
            "causal_links": causal_links,
            "hotspots": hotspots,
        }
