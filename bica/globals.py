import random
from typing import override

from bica.ms.interface import IMoralSchema
from .base import Action, ActionEffect, Actor, ActionId, Object, ObjectId, ActorId
from .intensions import InSpace
from utils import todo


class IGlobals:
    r: float
    space: InSpace
    actors: dict[ActorId, Actor]
    actions: dict[ActionId, Action]
    objects: dict[ObjectId, Object]

    def choose_action_and_target(self, probabilities: dict[tuple[ActionId, Object], float]) -> tuple[ActionId, Object]:
        todo()

    def execute(self, action_id: ActionId, author: Actor, target: Object) -> ActionEffect:
        todo()


class AbsGlobals(IGlobals):
    def __init__(self, r, space: InSpace):
        super().__init__()
        self.r = r
        self.space = space
    
    @override
    def choose_action_and_target(self, probabilities: dict[tuple[ActionId, Object], float]):
        return random.choices(
            list(probabilities.keys()),
            weights = list(probabilities.values()),
            k = 1
        )[0]
    
    

