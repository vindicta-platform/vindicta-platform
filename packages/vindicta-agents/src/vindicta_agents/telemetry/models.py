from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class GPUState(BaseModel):
    id: int
    name: str
    load: float = Field(..., description="GPU utilization (0-1)")
    memory_used: float = Field(..., description="VRAM used in MB")
    memory_total: float = Field(..., description="Total VRAM in MB")
    temperature: float = Field(..., description="Temperature in Celsius")


class CPUState(BaseModel):
    percent_per_core: List[float]
    total_percent: float
    frequency_current: float


class MemoryState(BaseModel):
    total: int
    available: int
    percent: float
    used: int


class HardwareState(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    cpu: CPUState
    memory: MemoryState
    gpus: List[GPUState] = Field(default_factory=list)


class ResourceUsage(BaseModel):
    """
    Standardized resource usage metrics for an agent or task.
    """

    cpu_percent: float
    memory_mb: float
    gpu_memory_mb: float = 0.0
