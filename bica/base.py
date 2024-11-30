from dataclasses import dataclass
from typing import Optional

from .intensions import InVec


type ActionId = str
type ObjectId = str
type ActorId = str
type Role = str


@dataclass(unsafe_hash=True)
class ActionEffect:
    on_author: InVec
    on_target: InVec
    author_weight: float = 1.0
    target_weight: float = 1.0


@dataclass(unsafe_hash=True)
class Object:
    id: ObjectId
    appraisal: InVec


class Actor(Object):
    pass


@dataclass(unsafe_hash=True)
class Action[Data]:
    id: ActionId
    data: Optional[Data] = None


@dataclass(unsafe_hash=True)
class ActionDetails:
    action: Action
    author: Actor
    target: Object|None
    tool: Object|None