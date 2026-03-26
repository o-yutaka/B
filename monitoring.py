import time
from typing import Dict

import psutil


class SystemMonitor:
    def __init__(self) -> None:
        self.start_time = time.time()
        self.completed_tasks = 0
        self.success_tasks = 0

    def mark_result(self, success: bool) -> None:
        self.completed_tasks += 1
        if success:
            self.success_tasks += 1

    def metrics(self, queue_size: int) -> Dict[str, float]:
        uptime = max(1.0, time.time() - self.start_time)
        throughput = self.completed_tasks / uptime
        success_rate = self.success_tasks / max(1, self.completed_tasks)
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.0),
            "memory_percent": psutil.virtual_memory().percent,
            "task_throughput": throughput,
            "success_rate": success_rate,
            "queue_size": queue_size,
        }
