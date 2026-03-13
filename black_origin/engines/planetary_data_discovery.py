from datetime import datetime, timezone


SEED_SOURCES = [
    {
        "name": "World Bank Indicators",
        "type": "api",
        "endpoint": "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL",
        "topic": "population",
    },
    {
        "name": "Open-Meteo Climate Archive",
        "type": "api",
        "endpoint": "https://archive-api.open-meteo.com/v1/archive",
        "topic": "climate",
    },
    {
        "name": "Our World In Data Energy",
        "type": "dataset",
        "endpoint": "https://ourworldindata.org/energy",
        "topic": "energy",
    },
]


class PlanetaryDataDiscoveryEngine:
    def discover(self, cycle: int):
        stamp = datetime.now(timezone.utc).isoformat()
        discoveries = []
        for index, source in enumerate(SEED_SOURCES):
            discoveries.append(
                {
                    "id": f"src-{cycle}-{index}",
                    "name": source["name"],
                    "source_type": source["type"],
                    "endpoint": source["endpoint"],
                    "topic": source["topic"],
                    "discovered_at": stamp,
                }
            )
        return discoveries
