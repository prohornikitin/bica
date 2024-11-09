from dataclasses import dataclass
from typing import Optional

from .intentionalities import InVec


type ActionId = str
type ActorId = str
type Role = str


@dataclass
class ActionEffect:
    on_author: InVec
    on_recipient: InVec
    weight: float = 1.0


@dataclass(unsafe_hash=True)
class Actor:
    id: ActorId
    appraisal: InVec

@dataclass
class Action[Data]:
    id: ActionId
    data: Optional[Data] = None

