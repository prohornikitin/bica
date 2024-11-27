from utils import todo; todo()

from typing import override

from bica.intensions import InSpace, InVec
from bica.ms.abstract import AbsMoralSchema
from bica.base import Action, ActionEffect, Actor
from bica.globals import AbsGlobals
from bica.ms.interface import MsState

class GlobalDefs(AbsGlobals):
    def __init__(self):
        super().__init__(0.1, InSpace([
            'dominance',
            'valence',
            'arouse',
        ]))
    
    @override
    def actions(self): #TODO вместо ActionId адекватное описание
        def makeInVec(data: list[float]):
            return InVec(self.space, data)

        return [
            Action(id='отругать', effect=ActionEffect(
                makeInVec([0.15, -0.05, -0.1]),
                makeInVec([-0.15, -0.1, 0.1]),
                0.2)
            ),
            Action(id='громко стукнуть', effect=ActionEffect(
                makeInVec([0.1, -0.05, 0.05]),
                makeInVec([-0.1, -0.05, 0.1]),
                0.2)
            )
        ]


globalDefs = GlobalDefs()

teacher = Actor(
    'teacher',
    InVec(globalDefs.space)
)

student = Actor(
    'student',
    InVec(globalDefs.space)
)


class StudyMs(AbsMoralSchema[str, str]):
    @override
    def state(self):
        actor = self.author()
        f = self.agency.feelings
        a = actor.appraisal.project(self.space)
        dist = (f - a).norm
        if dist < 0.1:
            return MsState.Normal
        elif dist < 0.5:
            return MsState.Active
        elif dist < 1:
            return MsState.Conflict
        else:
            return MsState.TemporaryInactive