from dataclasses import dataclass
import dataclasses
from typing import Any, Generic, TypeVar, override

from utils import todo

from ..intensions import InSpace, InVec

from .interface import Agency, Fabula, IMoralSchema, MsState
from ..base import Actor, Role


Node = TypeVar('Node')
PlanItem = TypeVar('PlanItem')


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