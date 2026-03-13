class KnowledgeGraphEngine:
    RELATIONSHIPS = ["produces", "consumes", "depends_on", "affects", "causes"]

    def update_graph(self, graph_state, normalized_entities):
        seen_entities = {node["name"] for node in graph_state["entities"]}
        for item in normalized_entities:
            if item["entity"] not in seen_entities:
                graph_state["entities"].append({"name": item["entity"], "category": item["topic"]})
                seen_entities.add(item["entity"])

        if len(graph_state["entities"]) > 1:
            a = graph_state["entities"][-2]
            b = graph_state["entities"][-1]
            relationship = {
                "source": a["name"],
                "target": b["name"],
                "type": self.RELATIONSHIPS[len(graph_state["relationships"]) % len(self.RELATIONSHIPS)],
            }
            if relationship not in graph_state["relationships"]:
                graph_state["relationships"].append(relationship)
        return graph_state
