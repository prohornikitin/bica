import random
from typing import override

from bica.ms.interface import IMoralSchema
from .base import Action, ActionEffect, Actor, ActionId, ActorId
from .intentionalities import InSpace
from utils import todo


class IGlobals:
    r: float
    space: InSpace

    def actions(self) -> list[Action]:
        todo()
    
    def actors(self) -> list[Actor]:
        todo()

    def actor_by_id(self, id: ActorId) -> Actor:
        todo()

    def choose_action_and_recipient(self, probabilities: dict[tuple[ActionId, Actor], float]) -> tuple[ActionId, Actor]:
        todo()

    def execute(self, action_id: ActionId, author: Actor, recipient: Actor) -> ActionEffect:
        todo()


class AbsGlobals(IGlobals):
    _moral_schemas: dict[ActorId, list[IMoralSchema]]

    def __init__(self, r, space: InSpace):
        super().__init__()
        self.r = r
        self.space = space
    
    @override
    def choose_action_and_recipient(self, probabilities: dict[tuple[ActionId, Actor], float]):
        return random.choices(
            list(probabilities.keys()),
            weights = list(probabilities.values()),
            k = 1
        )[0]
    
    

