from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class KernelHeartbeat:
    cycle: int
    alive: bool
    timestamp: str


class KernelEngine:
    def __init__(self) -> None:
        self.cycle = 0
        self.system_alive = True

    def tick(self) -> KernelHeartbeat:
        self.cycle += 1
        return KernelHeartbeat(
            cycle=self.cycle,
            alive=self.system_alive,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
