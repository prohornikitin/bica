from dataclasses import dataclass, field as field_init
from enum import StrEnum, auto
from typing import Any, Generic, TypeVar
from utils import todo

from ..intensions import InSpace, InVec
from ..base import ActionId, Actor, Role

    
class MsState(StrEnum):
    Active = auto(),
    Normal = auto(),
    Conflict = auto(),
    Inactive = auto(),

@dataclass
class Agency():
    perspective: Role
    feelings: InVec
    mood: Any = None


Node = TypeVar('Node')
PlanItem = TypeVar('PlanItem')


@dataclass
class Fabula(Generic[Node, PlanItem]):
    nodes: list[Node] = field_init(default_factory = list)
    connections: dict[Node, tuple[Node]] = field_init(default_factory = dict)
    plan: list[PlanItem] = field_init(default_factory = list)

class IMoralSchema:
    actors_binded_to_roles: dict[Role, Actor]
    space: InSpace
    agency: Agency
    fabula: Fabula[Node, PlanItem]

    def calc_likelihood(self, actionId: ActionId, target: Actor) -> float:
        todo()
    
    #only called if schema is active
    def after_action(self) -> None:
        todo()

    def author(self) -> Actor:
        todo()
    
    def state(self) -> MsState: 
        todo()
        

