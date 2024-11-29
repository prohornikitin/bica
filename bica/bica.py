from collections.abc import Callable, Iterable
from dataclasses import dataclass
import logging
from typing import Optional

from bica.intensions import InVec

from .base import ActionEffect, Actor, Object, ObjectId, ActionId
from .globals import IGlobals
from .ms.interface import IMoralSchema, MsState


logger = logging.getLogger(__name__)


@dataclass
class ActionRequest:
    author_id: ObjectId
    constraint: Callable[[ActionId, Object], bool] = lambda x,y: True


class Bica:
    _moral_schemas: dict[ObjectId, list[IMoralSchema]]
    _globals: IGlobals

    def __init__(self,
        moral_schemas: dict[ObjectId, list[IMoralSchema]],
        globals: IGlobals
    ):
        self._moral_schemas = moral_schemas
        self._globals = globals

    def execute_request(self, req: ActionRequest) -> Optional[tuple[ActionId, Object]]:
        active_schemas = list(filter(
            lambda ms: ms.state() not in {MsState.Inactive}, 
            self._moral_schemas.get(req.author_id, [])
        ))
        if len(active_schemas) == 0:
            logger.warning(f"no active moral schemas for author '{req.author_id}'")
            return None
            
        probabilities = self._calc_probabilities(active_schemas, req.constraint)
        action_id, target = self._globals.choose_action_and_target(probabilities)
        author = self._globals.actors[req.author_id]
        effect = self._globals.execute(action_id, author, target)
        self._apply_bica_effect(effect, author, author)
        not_inactive_schemas = filter(
            lambda ms: (ms.state() not in {MsState.Inactive}) and
            (ms.author().id == author.id or ms.author().id == target.id),
            self._moral_schemas.get(req.author_id, [])
        )
        
        for ms in not_inactive_schemas:
            ms.after_action()
        return action_id, target
    
    def _apply_bica_effect(self, effect: ActionEffect, author: Actor, target: Object) -> None:
        author.appraisal = self._calc_new_appraisal(author, effect.on_author, self._globals.r * effect.author_weight)
        target.appraisal = self._calc_new_appraisal(target, effect.on_target, self._globals.r * effect.target_weight)
    
    def _calc_new_appraisal(self, actor: Object, effect: InVec, r: float) -> InVec:
        return effect * r + actor.appraisal * (1 - r)

    def _calc_probabilities(self,
        schemas: Iterable[IMoralSchema],
        constraint: Callable[[ActionId, Object], bool] = lambda x, y: True,
    ) -> dict[tuple[ActionId, Object], float]:
        likelihoods: dict[tuple[ActionId, Object], float] = dict()
        for ms in schemas:
            for action_id in self._globals.actions.keys():
                for target in self._globals.objects.values():
                    if not constraint(action_id, target):
                        continue
                    key = (action_id, target)
                    l = likelihoods.setdefault(key, 0)
                    likelihoods[key] = l + ms.calc_likelihood(action_id, target)
        if len(likelihoods) == 0:
            return likelihoods
        likelihood_sum = sum(likelihoods.values(), 0)
        for k, v in likelihoods.items():
            likelihoods[k] = v / likelihood_sum
        return likelihoods