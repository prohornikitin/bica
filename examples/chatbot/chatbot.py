from dataclasses import dataclass
from enum import StrEnum, auto
from functools import reduce
from typing import override

from bica.intentionalities import InSpace, InVec
from bica.ms.abstract import AbsMoralSchema, Agency, Fabula
from bica.base import Action, Actor, ActorId, ActionId, ActionEffect
from bica.globals import AbsGlobals, IGlobals
from bica.ms.interface import MsState
from bica.main import ActionRequest, Main
from .intentionalities import intensional_calc
from .gpt import gpt, Message
from . import prompts



class ActionIdEnum(StrEnum):
    user_talk = auto()
    acquaintance_talk = auto()
    acquaintance_to_interests_talk = auto()
    interests_talk = auto()
    interests_to_common_interests_talk = auto()
    common_interests_talk = auto()
    finish_talk = auto()


@dataclass
class TalkPhase:
    available_action: ActionIdEnum
    initial_feelings: InVec

    def __hash__(self):
        return id(self)

@dataclass
class FabulaNode:
    state: dict[ActorId, TalkPhase]

    def __hash__(self):
        return id(self)


phases = [
    TalkPhase(ActionIdEnum.acquaintance_talk,
        InVec(InSpace({
            'коммуникативность',
            'дружелюбность',
            'любознательность',
            'внимательность',
            'инициативность',
        }), [0.7, 0.7, 0.4, 0.5, 0.6]),
    ),
    TalkPhase(ActionIdEnum.interests_talk,
        InVec(InSpace({
            'уверенность',
            'критичность',
            'инициативность',
            'заботливость',
            'внимательность',
            'коммуникабельность',
        }), [0.6, 0.0, 0.6, 0.2, 0.5, 0.7]),
    ),
    TalkPhase(ActionIdEnum.common_interests_talk,
        InVec(InSpace({
            'коммуникабельность',
            'целеустремленность',
            'оптимизм',
            'амбициозность',
            'проницательность',
        }), [0.5, 0.5, 0.4, 0.5, 0.2]),
    ),
    TalkPhase(ActionIdEnum.finish_talk,
        InVec(InSpace(set())),
    ),
]


axes = map(lambda x: x.initial_feelings.space.axes, phases)
global_space = InSpace(reduce(lambda acc, x: acc|x, axes))


ai = Actor('ai', InVec(global_space))
users = [
    Actor(f'user_{i+1}', InVec(global_space)) for i in range(3)
]


class GlobalDefs(AbsGlobals):
    def __init__(self, space: InSpace, Actors: list[Actor]):
        super().__init__(0.1, space)
        self._actors = [ai] + users
        self.messages = [Message('assistant', prompts.initial)]
    
    @override
    def actions(self) -> list[Action]:
        return list(map(Action, ActionIdEnum))
    
    @override
    def actors(self):
        return self._actors
    
    @override
    def actor_by_id(self, id: ActorId) -> Actor:
        return next(filter(lambda x: x.id == id, self.actors()))

    @override
    def execute(self, action_id: ActionId, author: Actor, recipient: Actor) -> ActionEffect:
        if author.id == 'ai':
            return self.ai_action(action_id, author, recipient)
        else:
            return self.user_action(action_id, author)
    
    def ai_action(self, action_id: ActionId, author: Actor, recipient: Actor) -> ActionEffect:
        if action_id == ActionIdEnum.acquaintance_talk:
            prompt = prompts.phase1
        elif action_id == ActionIdEnum.acquaintance_to_interests_talk:
            prompt = prompts.from1to2 + prompts.phase2
        elif action_id == ActionIdEnum.interests_talk:
            prompt = prompts.phase2
        elif action_id == ActionIdEnum.interests_to_common_interests_talk:
            prompt = prompts.from2to3
        elif action_id == ActionIdEnum.common_interests_talk:
            prompt = prompts.phase3
        elif action_id == ActionIdEnum.finish_talk:
            prompt = prompts.phase_finish
        prompt = prompts.changed_message(self.messages[-1]) + prompt
        reply = gpt(self.messages + [Message('assistant', prompt)])
        print(f'{author.id} say: {reply}')
        self.messages.append(Message('assistant', reply))
        return ActionEffect(InVec(self.space), InVec(self.space))

    def user_action(self, action_id: ActionId, author: Actor) -> ActionEffect:
        text = input(f'{author.id} say: ')
        self.messages.append(Message('user', text))
        phase = phases[0]
        if action_id == ActionIdEnum.common_interests_talk:
            phase = phases[1]
        elif action_id == ActionIdEnum.common_interests_talk:
            phase = phases[2]
        space = phase.initial_feelings.space
        effect = intensional_calc(space, text).unproject(InVec(self.space))
        return ActionEffect(InVec(self.space), effect)

globalDefs = GlobalDefs(global_space, [ai] + users)


fabula_nodes = [
    FabulaNode({
        users[0].id: phases[i//9],
        users[1].id: phases[i//3 % 3],
        users[2].id: phases[i % 3]
    }) for i in range(3**3)
]

fabula_connections = dict()
for i in range(3**3-1):
    fabula_connections.update({fabula_nodes[i]: [fabula_nodes[i+1]]})
    if i+3 < 3**3:
        fabula_connections.update({fabula_nodes[i]: [fabula_nodes[i+3]]})
    if i+9 < 3**3:
        fabula_connections.update({fabula_nodes[i]: [fabula_nodes[i+9]]})




class CommonAiMs(AbsMoralSchema[None, None]):
    _globals: IGlobals

    def __init__(self,
        globals: IGlobals,
        user: Actor,
        fabula: Fabula[FabulaNode, TalkPhase]
    ):
        initial_feelings = fabula.plan[0].initial_feelings
        super().__init__(
            initial_feelings.space,
            {'ai': ai, 'user': user},
            Agency('ai', initial_feelings.copy()),
            fabula
        )
        self._globals = globals

    @override
    def calc_likelihood(self, actionId: ActionId, recipient: Actor) -> float:
        available_action = self.fabula.plan[0].available_action 
        if actionId == available_action and recipient != self.author():
            return 1.0
        else:
            return 0.0

    @override
    def after_action(self) -> None:
        state = self.state()
        if state == MsState.Conflict:
            self._feelings_dynamic()
        if state == MsState.Normal:
            self._next_step()

    def _next_step(self):
        self.fabula.plan = self.fabula.plan[1:]
        current_phase = self.fabula.plan[0]
        self.space = current_phase.initial_feelings.space
        self.agency.feelings = current_phase.initial_feelings
        

    @override
    def _feelings_dynamic(self) -> None:
        author = self.author()
        p = 0.08
        f = self.agency.feelings
        a = author.appraisal.project(self.space)
        self.agency.feelings = (1 - p) * f  + p * (a - f)

    @override
    def state(self):
        actor = self.author()
        f = self.agency.feelings
        a = actor.appraisal.project(self.space)
        dist = (f - a).norm()
        if dist < 0.25:
            if len(self.fabula.plan) != 1:
                return MsState.Normal
            else:
                return MsState.Inactive
        else:
            return MsState.Conflict


class UserMs(AbsMoralSchema[None, None]):
    _globals: IGlobals

    def __init__(self,
        globals: IGlobals,
        user: Actor,
    ):
        space = globals.space
        super().__init__(
            space,
            {'ai': ai, 'user': user},
            Agency('ai', InVec(space)),
            Fabula()
        )
        self._globals = globals

    @override
    def calc_likelihood(self, actionId: ActionId, recipient: Actor) -> float:
        if actionId == ActionIdEnum.user_talk:
            return 1.0
        else:
            return 0.0

    @override
    def after_action(self) -> None:
        pass

    @override
    def state(self):
        return MsState.Active


schemas = {
    ai.id: [
        CommonAiMs(
            globalDefs,
            users[i], 
            Fabula(fabula_nodes, fabula_connections, phases)
        ) for i in range(3)
    ],
    users[0].id: [UserMs(globalDefs, users[0])],
    users[1].id: [UserMs(globalDefs, users[1])],
    users[2].id: [UserMs(globalDefs, users[2])],
}

bica = Main(schemas, globalDefs)

while True:
    response = bica.execute_request(ActionRequest(ai.id))
    if response is None:
        break
    _, recipient = response
    bica.execute_request(ActionRequest(recipient.id))

print('goal achieved')