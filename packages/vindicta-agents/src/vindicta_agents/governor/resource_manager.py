from typing import Dict
from ..telemetry.monitor import HardwareMonitor
from .models import PriorityLevel, ComputeQuota, ThrottlingDecision
from ..utils.logger import logger


class ResourceGovernor:
    """
    Manages compute quotas and enforces resource limits based on hardware telemetry.
    """

    def __init__(self, monitor: HardwareMonitor):
        self.monitor = monitor
        # Thresholds
        self.max_cpu_percent = 90.0
        self.max_memory_percent = 85.0
        self.max_gpu_memory_percent = 90.0
        self.max_gpu_temp_c = 80.0

        # State
        self.active_tasks: Dict[str, ComputeQuota] = {}

    def check_resources(self, priority: PriorityLevel) -> ThrottlingDecision:
        """
        Determines if a new task should be allowed to start based on current system load.
        """
        state = self.monitor.get_latest_state()
        if not state:
            return ThrottlingDecision(should_throttle=False)

        # 1. Thermal Throttling (Highest Priority Check)
        for gpu in state.gpus:
            if gpu.temperature >= self.max_gpu_temp_c:
                logger.warning(
                    "governor_throttle",
                    type="thermal",
                    gpu_id=gpu.id,
                    temp=gpu.temperature,
                )
                return ThrottlingDecision(
                    should_throttle=True,
                    reason=f"Thermal Throttling: GPU {gpu.id} at {gpu.temperature}C",
                    suggested_wait_time=5.0,
                )

        # 2. CPU Pressure (Newly added)
        if state.cpu.total_percent >= self.max_cpu_percent:
            if priority not in [PriorityLevel.CRITICAL, PriorityLevel.HIGH]:
                logger.warning(
                    "governor_throttle", type="cpu", usage=state.cpu.total_percent
                )
                return ThrottlingDecision(
                    should_throttle=True,
                    reason=f"CPU Pressure: {state.cpu.total_percent}% used",
                    suggested_wait_time=3.0,
                )

        # 3. Memory Pressure
        if state.memory.percent >= self.max_memory_percent:
            if priority in [PriorityLevel.LOW, PriorityLevel.IDLE]:
                logger.warning(
                    "governor_throttle", type="memory", usage=state.memory.percent
                )
                return ThrottlingDecision(
                    should_throttle=True,
                    reason=f"Memory Pressure: {state.memory.percent}% used",
                    suggested_wait_time=2.0,
                )

        # 4. VRAM Pressure
        for gpu in state.gpus:
            if gpu.memory_total > 0:
                vram_percent = (gpu.memory_used / gpu.memory_total) * 100
                if vram_percent >= self.max_gpu_memory_percent:
                    if priority != PriorityLevel.CRITICAL:
                        logger.warning(
                            "governor_throttle",
                            type="vram",
                            gpu_id=gpu.id,
                            usage=vram_percent,
                        )
                        return ThrottlingDecision(
                            should_throttle=True,
                            reason=f"VRAM Pressure: GPU {gpu.id} at {vram_percent:.1f}%",
                            suggested_wait_time=1.0,
                        )

        return ThrottlingDecision(should_throttle=False)

    def allocate_resources(self, task_id: str, quota: ComputeQuota) -> bool:
        """
        Allocates resources for a task. Returns True if successful.
        """
        self.active_tasks[task_id] = quota
        logger.debug("resource_allocated", task_id=task_id)
        return True

    def release_resources(self, task_id: str):
        """
        Releases resources for a task.
        """
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
            logger.debug("resource_released", task_id=task_id)
