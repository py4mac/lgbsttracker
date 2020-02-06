from datetime import datetime

from pydantic import BaseModel


class ExperimentAction:
    NONE = "none"
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"


class ExperimentState:
    STOPPED = "stopped"
    FAILED = "failed"
    RUNNING = "running"
    FINISHED = "finished"


# Shared properties
class ExperimentBase(BaseModel):
    experiment_uuid: str = None  # type: ignore
    ts: datetime = None  # type: ignore
    action: str = None  # type: ignore
    vision_sensor: float = None  # type: ignore
    speed: float = None  # type: ignore
    state: str = None  # type: ignore


# Properties to receive on experiment creation
class ExperimentCreate(ExperimentBase):
    experiment_uuid: str


# Properties to receive on item update
class ExperimentUpdate(ExperimentBase):
    pass


# Properties shared by models stored in DB
class ExperimentInDBBase(ExperimentBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Experiment(ExperimentInDBBase):
    pass


# Properties properties stored in DB
class ExperimentInDB(ExperimentInDBBase):
    pass
