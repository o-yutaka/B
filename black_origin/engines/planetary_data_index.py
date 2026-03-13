from typing import Dict, List


class PlanetaryDataIndexEngine:
    def update_index(self, index_state: Dict, discoveries: List[Dict]) -> Dict:
        datasets = [d for d in discoveries if d["source_type"] == "dataset"]
        apis = [d for d in discoveries if d["source_type"] == "api"]

        seen_entities = {entity["name"] for entity in index_state["entities"]}
        seen_topics = set(index_state["topics"])

        for item in discoveries:
            entity_name = item["name"].split()[0]
            if entity_name not in seen_entities:
                index_state["entities"].append({"name": entity_name, "origin": item["name"]})
                seen_entities.add(entity_name)
            if item["topic"] not in seen_topics:
                index_state["topics"].append(item["topic"])
                seen_topics.add(item["topic"])

        index_state["datasets"] = self._dedupe(index_state["datasets"] + datasets)
        index_state["apis"] = self._dedupe(index_state["apis"] + apis)
        return index_state

    @staticmethod
    def _dedupe(items: List[Dict]) -> List[Dict]:
        unique = {}
        for item in items:
            unique[item["name"]] = item
        return list(unique.values())
