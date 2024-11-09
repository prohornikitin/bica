from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import chain
import logging
from typing import Optional

from bica.intentionalities import InVec

from .base import ActionEffect, Actor, ActorId, ActionId
from .globals import IGlobals
from .ms.interface import IMoralSchema, MsState


logger = logging.getLogger(__name__)


@dataclass
class ActionRequest:
    author: ActorId
    constraint: Callable[[ActionId, Actor], bool] = lambda x,y: True

class Main:
    _moral_schemas: dict[ActorId, list[IMoralSchema]]
    _globals: IGlobals

    def __init__(self,
        moral_schemas: dict[ActorId, list[IMoralSchema]],
        globals: IGlobals
    ):
        self._moral_schemas = moral_schemas
        self._globals = globals

    def execute_request(self, req: ActionRequest) -> Optional[tuple[ActionId, Actor]]:
        active_schemas = list(filter(
            lambda ms: ms.state() not in {MsState.Inactive}, 
            self._moral_schemas.get(req.author, [])
        ))
        if len(active_schemas) == 0:
            logger.warning(f"no active moral schemas for author '{req.author}'")
            return
            
        probabilities = self._calc_probabilities(active_schemas, req.constraint)
        action_id, recipient = self._globals.choose_action_and_recipient(probabilities)
        author = self._globals.actor_by_id(req.author)
        effect = self._globals.execute(action_id, author, recipient)
        self._apply_bica_effect(effect, author, author)
        not_inactive_schemas = filter(
            lambda ms: (ms.state() not in {MsState.Inactive}) and
            (ms.author().id == author.id or ms.author().id == recipient.id),
            self._moral_schemas.get(req.author, [])
        )
        
        for ms in not_inactive_schemas:
            ms.after_action()
        return action_id, recipient
    
    def _apply_bica_effect(self, effect: ActionEffect, author: Actor, recipient: Actor) -> None:
        author.appraisal = self._calc_new_appraisal(author, effect.on_author, self._globals.r)
        recipient.appraisal = self._calc_new_appraisal(recipient, effect.on_recipient, self._globals.r)
    
    def _calc_new_appraisal(self, actor: Actor, effect: InVec, r: float) -> InVec:
        return effect * r + actor.appraisal * (1 - r)

    def _calc_probabilities(self,
        schemas: Iterable[IMoralSchema],
        constraint: Callable[[ActionId, Actor], bool] = lambda x, y: True,
    ) -> dict[tuple[ActionId, Actor], float]:
        likelihoods: dict[tuple[ActionId, Actor], float] = dict()
        for ms in schemas:
            for action in self._globals.actions():
                for recipient in self._globals.actors():
                    if not constraint(action.id, recipient):
                        continue
                    key = (action.id, recipient)
                    l = likelihoods.setdefault(key, 0)
                    likelihoods[key] = l + ms.calc_likelihood(action.id, recipient)
        if len(likelihoods) == 0:
            return likelihoods
        likelihood_sum = sum(likelihoods.values(), 0)
        for k, v in likelihoods.items():
            likelihoods[k] = v / likelihood_sum
        return likelihoods