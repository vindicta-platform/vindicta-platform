import psutil
import asyncio
from typing import List, Optional, Callable
from datetime import datetime
from .models import HardwareState, CPUState, MemoryState, GPUState
from ..utils.logger import logger


class HardwareMonitor:
    """
    Monitors system hardware resources (CPU, Memory, GPU).
    Maintains a 1Hz heartbeat to track system health.
    """

    def __init__(self, polling_interval: float = 1.0):
        self.polling_interval = polling_interval
        self._running = False
        self._latest_state: Optional[HardwareState] = None
        self._callbacks: List[Callable[[HardwareState], None]] = []

    def start(self):
        """Starts the monitoring loop."""
        self._running = True
        asyncio.create_task(self._monitor_loop())

    def stop(self):
        """Stops the monitoring loop."""
        self._running = False

    def register_callback(self, callback: Callable[[HardwareState], None]):
        """Registers a callback to receive hardware state updates."""
        self._callbacks.append(callback)

    def get_latest_state(self) -> Optional[HardwareState]:
        """Returns the most recent hardware state."""
        return self._latest_state

    async def _monitor_loop(self):
        while self._running:
            try:
                state = self._collect_metrics()
                self._latest_state = state

                # Notify callbacks
                for callback in self._callbacks:
                    try:
                        callback(state)
                    except Exception as e:
                        logger.error("monitor_callback_error", error=str(e))

                await asyncio.sleep(self.polling_interval)
            except Exception as e:
                logger.error("metrics_collection_error", error=str(e))
                await asyncio.sleep(self.polling_interval)

    def _collect_metrics(self) -> HardwareState:
        # CPU
        cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
        cpu_total = psutil.cpu_percent(interval=None)
        cpu_freq = psutil.cpu_freq()
        current_freq = cpu_freq.current if cpu_freq else 0.0

        cpu_state = CPUState(
            percent_per_core=cpu_per_core,
            total_percent=cpu_total,
            frequency_current=current_freq,
        )

        # Memory
        mem = psutil.virtual_memory()
        memory_state = MemoryState(
            total=mem.total, available=mem.available, percent=mem.percent, used=mem.used
        )

        # GPU
        gpus = []
        try:
            import GPUtil

            gpu_list = GPUtil.getGPUs()
            for gpu in gpu_list:
                gpus.append(
                    GPUState(
                        id=gpu.id,
                        name=gpu.name,
                        load=gpu.load,
                        memory_used=gpu.memoryUsed,
                        memory_total=gpu.memoryTotal,
                        temperature=gpu.temperature,
                    )
                )
        except ImportError:
            # Expected if GPUtil is not installed in the current environment
            pass
        except Exception as e:
            logger.debug("gpu_metrics_collection_failed", error=str(e))

        return HardwareState(
            timestamp=datetime.now(), cpu=cpu_state, memory=memory_state, gpus=gpus
        )
