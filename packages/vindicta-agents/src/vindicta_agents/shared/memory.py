from typing import Dict, Any
from pydantic import BaseModel, Field
import uuid


class BoardState(BaseModel):
    """
    Canonical Board State.
    Represents the 'Table Top' shared memory.
    """

    version: uuid.UUID = Field(default_factory=uuid.uuid4)
    units: Dict[str, Any] = Field(default_factory=dict)  # str = unit_id
    phase: str = "Deployment"
    turn: int = 1

    def update(self, delta: Dict[str, Any]) -> None:
        """
        Updates the board state with a delta.
        Only the Supervisor should call this.
        """
        if "units" in delta:
            self.units.update(delta["units"])
        if "phase" in delta:
            self.phase = delta["phase"]
        if "turn" in delta:
            self.turn = delta["turn"]
        self.version = uuid.uuid4()


class SharedMemory:
    """
    Singleton manager for the Board State.
    """

    _instance = None
    _state: BoardState = BoardState()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedMemory, cls).__new__(cls)
            cls._state = BoardState()
        return cls._instance

    @property
    def state(self) -> BoardState:
        return self._state

    def reset(self):
        self._state = BoardState()
