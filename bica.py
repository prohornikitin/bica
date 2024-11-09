from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, Tuple, TypeAlias, TypeVar

from numpy.typing import NDArray

from utils import todo

Role: TypeAlias = str
Appraisal: TypeAlias = NDArray
Feelings: TypeAlias = NDArray
ActionId: TypeAlias = str
ActorId: TypeAlias = str

@dataclass
class Action:
    id: ActionId
    effect_on_author: Appraisal
    effect_on_recipient: Appraisal
    weight: float

@dataclass
class Actor:
    id: ActorId
    appraisal: Appraisal
    feelings: Feelings

class IMoralSchema:
    def actions_and_recipients(self) -> Iterable[Tuple[ActionId, Actor]]:
        todo()

    def calc_likelihood(self, action: ActionId, recipient: Actor) -> float:
        todo()
    
    # includes learning and applying bica effects.
    def execute(self, id: ActionId, recipient: Actor) -> None:
        todo()
    
    def is_applicable(self) -> bool:
        todo()



Objective = TypeVar('Objective')
@dataclass
class Agency(Generic[Objective]):
    mood: Any
    perspective: Tuple[Role, Actor]
    objective: Objective

Node = TypeVar('Node')
Plan = TypeVar('Plan')
Condition = Callable[[Dict[Role, Actor]], bool]
@dataclass
class Fabula(Generic[Node, Plan]):
    story: List[Node]
    connections: Dict[Node, Tuple[Tuple[Condition, Node]]]
    plan: Plan

class AbsMoralSchema(IMoralSchema, Generic[Node, Plan, Objective]):
    actors: Dict[Role, Actor]
    fabula: Fabula[Node, Plan]
    agency: Agency[Objective]
    r: float

    def __init__(self, interface = None, fabula = None, agency = None):
        super().__init__()
        self.interface = interface
        self.fabula = fabula
        self.agency = agency
    
    def execute(self, id: ActionId, recipient: Actor) -> None:
        self._execute_bica_effects(id, recipient)

    def _get_action_by_id(self, id: ActionId) -> Optional[Action]:
        todo()
    
    def _execute_bica_effects(self, action_id: ActionId, recipient: Actor) -> None:
        action = self._get_action_by_id(action_id)
        if action is None:
            return
        author = self.agency.perspective[1]
        author.appraisal = calc_new_author_appraisal(author, action, self.r)
        recipient.appraisal = calc_new_recipient_appraisal(recipient, action, self.r)
        self._feelings_dynamic_if_needed()

    def _feelings_dynamic_if_needed(self):
        todo()


def choose_action_and_recipient(schemas: Iterable[IMoralSchema]) -> Tuple[ActionId, Actor]:
    likelihoods: Dict[Tuple[ActionId, Actor], float] = dict()
    for ms in schemas:
        for actionId, recipient in ms.actions_and_recipients():
            key = (actionId, recipient)
            l = likelihoods.setdefault(key, 0)
            likelihoods[key] = l + ms.calc_likelihood(actionId, recipient)
    return max(likelihoods.items(), key = lambda x: x[1])[0]



def calc_new_author_appraisal(author: Actor, action: Action, r: float) -> Appraisal:
    return action.effect_on_author * r * action.weight + author.appraisal * (1 - r * action.weight)


def calc_new_recipient_appraisal(recipient: Actor, action: Action, r: float) -> Appraisal:
    return action.effect_on_recipient * r * action.weight + recipient.appraisal * (1 - r * action.weight)