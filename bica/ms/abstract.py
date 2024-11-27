from dataclasses import dataclass
import dataclasses
from typing import Any, Generic, TypeVar, override

from utils import todo

from ..intensions import InSpace, InVec

from .interface import IMoralSchema, MsState
from ..base import Actor, Role


@dataclass
class Agency():
    perspective: Role
    feelings: InVec
    mood: Any = None


Node = TypeVar('Node')
PlanItem = TypeVar('PlanItem')


@dataclass
class Fabula(Generic[Node, PlanItem]):
    nodes: list[Node] = dataclasses.field(default_factory = list)
    connections: dict[Node, tuple[Node]] = dataclasses.field(default_factory = dict)
    plan: list[PlanItem] = dataclasses.field(default_factory = list)

class AbsMoralSchema(IMoralSchema, Generic[Node, PlanItem]):
    actors_binded_to_roles: dict[Role, Actor]
    space: InSpace
    agency: Agency
    fabula: Fabula[Node, PlanItem]

    def __init__(
        self,
        space: InSpace,
        actors_binded_to_roles: dict[Role, Actor],
        agency: Agency,
        fabula: Fabula[Node, PlanItem] = Fabula(),
    ):
        super().__init__()
        self.space = space
        self.actors_binded_to_roles = actors_binded_to_roles
        self.agency = agency
        self.fabula = fabula
    
    @override
    def author(self) -> Actor:
        author_role = self.agency.perspective
        return self.actors_binded_to_roles[author_role]
        
    def _feelings_dynamic(self) -> None:
        todo()
    
    @override
    def state(self) -> MsState:
        todo()

    @override
    def after_action(self) -> None:
        state = self.state()
        if state == MsState.Conflict:
            self._feelings_dynamic()