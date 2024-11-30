from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import chain
import logging
from typing import Optional

from bica.intensions import InVec

from .base import ActionDetails, ActionEffect, Actor, Object, ObjectId, ActionId, ActorId
from .globals import IGlobals
from .ms.interface import IMoralSchema, MsState


logger = logging.getLogger(__name__)


class Bica:
    _moral_schemas: dict[ObjectId, list[IMoralSchema]]
    _globals: IGlobals

    def __init__(self,
        moral_schemas: dict[ActorId, list[IMoralSchema]],
        globals: IGlobals
    ):
        self._moral_schemas = moral_schemas
        self._globals = globals

    def execute_action(self,
        constraint: Callable[[ActionDetails], bool] = lambda d: True
    ) -> Optional[ActionDetails]:
        likelihoods = self._calc_likelihoods(constraint)
        if len(likelihoods) == 0:
            return None
        probabilities = self._probabilities(likelihoods)
        if len(probabilities) == 0:
            return None
        chosen = self._globals.choose_action_and_target(probabilities)
        effect = self._globals.execute(chosen)
        author = chosen.author
        target = chosen.target
        self._apply_bica_effect(effect, author, target)
        not_inactive_schemas = filter(
            lambda ms: (ms.state() not in {MsState.Inactive}) and
            (ms.author().id == author.id or ms.author().id == target.id),
            self._moral_schemas.get(author.id, [])
        )
        
        for ms in not_inactive_schemas:
            ms.after_action()
        return chosen
        
    def _apply_bica_effect(self,
        effect: ActionEffect,
        author: Actor,
        target: Object|None
    ) -> None:
        author.appraisal = self._calc_new_appraisal(author, effect.on_author, self._globals.r * effect.author_weight)
        if target is None:
            return
        target.appraisal = self._calc_new_appraisal(target, effect.on_target, self._globals.r * effect.target_weight)
    
    def _calc_new_appraisal(self, actor: Object, effect: InVec, r: float) -> InVec:
        return effect * r + actor.appraisal * (1 - r)

    def _calc_likelihoods(self,
        constraint: Callable[[ActionDetails], bool]
    ) -> dict[ActionDetails, float]:
        likelihoods: dict[ActionDetails, float] = dict()
        for author in self._globals.actors.values():
            active_schemas = list(filter(
                lambda ms: ms.state() not in {MsState.Inactive}, 
                self._moral_schemas.get(author.id, [])
            ))
            # if len(active_schemas) == 0:
            #     logger.warning(f"no active moral schemas for author '{author.id}'")
            for ms in active_schemas:
                for action in self._globals.actions.values():
                    for target in chain(self._globals.objects.values(), [None]):
                        for tool in chain(self._globals.objects.values(), [None]):
                            details = ActionDetails(action, ms.author(), target, tool)
                            if not constraint(details):
                                continue
                            l = likelihoods.setdefault(details, 0)
                            likelihoods[details] = l + ms.calc_likelihood(details)
        return likelihoods
        
    def _probabilities(self, likelihoods: dict[ActionDetails, float]) -> dict[ActionDetails, float]:
        if len(likelihoods) == 0:
            return likelihoods
        probabilities = dict()
        likelihood_sum = sum(likelihoods.values(), 0)
        if likelihood_sum == 0:
            return probabilities
        for k, v in likelihoods.items():
            probabilities[k] = v / likelihood_sum
        return likelihoods