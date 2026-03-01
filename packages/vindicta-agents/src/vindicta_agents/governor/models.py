from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import Optional


class PriorityLevel(Enum):
    CRITICAL = auto()  # Live Match Inference
    HIGH = auto()  # Active User Interaction
    NORMAL = auto()  # Standard Tasks
    LOW = auto()  # Background Training / Analysis
    IDLE = auto()  # Maintenance


class ComputeQuota(BaseModel):
    """
    Defines the resource limits for a specific task or agent.
    """

    max_cpu_percent: float = Field(..., description="Max CPU usage allowed (%)")
    max_memory_mb: float = Field(..., description="Max RAM allowed (MB)")
    max_gpu_memory_mb: float = Field(0.0, description="Max VRAM allowed (MB)")
    time_limit_seconds: Optional[float] = Field(None, description="Max execution time")


class ThrottlingDecision(BaseModel):
    should_throttle: bool
    reason: Optional[str] = None
    suggested_wait_time: float = 0.0
