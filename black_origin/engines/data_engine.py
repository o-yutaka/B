class DataEngine:
    def normalize_entities(self, discoveries):
        normalized = []
        for item in discoveries:
            normalized.append(
                {
                    "entity": item["name"],
                    "topic": item["topic"],
                    "source": item["endpoint"],
                }
            )
        return normalized
