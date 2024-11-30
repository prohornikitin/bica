from random import sample
from typing import override
from bica.base import ActionDetails, ActionEffect, Actor, Object
from bica.bica import Bica
from bica.globals import AbsGlobals
from bica.intensions import InVec
from bica.ms.abstract import AbsMoralSchema, Agency, Fabula
from bica.ms.interface import MsState
from .intensions import space, vec
from .actors import ObjectData, allObjects, object_groups, whiteface, redhead, rat, obj_data
from .actions import ActionData, actions


class GlobalDefs(AbsGlobals):
    def __init__(self, r: float):
        super().__init__(r, space)
        self.actors = dict(map(lambda a: (a.id, a), object_groups['actor']))
        self.objects = dict(map(lambda o: (o.id, o), allObjects))
        self.actions = dict(map(lambda a: (a.id, a), actions))
        self.fabula = Fabula()

    @override
    def execute(self, details: ActionDetails) -> ActionEffect:
        actionData: ActionData = details.action.data
        if actionData.author_next_pos == 'random':
            author_next_pos = sample(['on the floor', 'trash', 'plate'], k=1)[0]
        else:
            author_next_pos = actionData.author_next_pos
        if actionData.author_next_pos is not None:
            obj_data[details.author.id].state.pos = author_next_pos
        if actionData.author_next_state is not None:
            obj_data[details.author.id].state.state = actionData.author_next_state
        other = obj_data[details.author.id].state.other
        next_other = actionData.author_followup
        if next_other is not None:
            if next_other.startswith('not'):
                next_other_opposite = next_other.replace('not ','')
            elif next_other is not None:
                next_other_opposite = f'not {next_other}'
            try:
                other.remove(next_other_opposite)
            except ValueError:
                pass
            other.append(next_other)
        if details.target is not None:
            if actionData.target_next_pos is not None:
                obj_data[details.target.id].state.pos = actionData.target_next_pos
            if actionData.target_next_state is not None:
                obj_data[details.target.id].state.state = actionData.target_next_state
            other = obj_data[details.target.id].state.other
            next_other = actionData.target_followup
            if next_other is not None:
                if next_other.startswith('not'):
                    next_other_opposite = next_other.replace('not ','')
                elif next_other is not None:
                    next_other_opposite = f'not {next_other}'
                try:
                    other.remove(next_other_opposite)
                except ValueError:
                    pass
                other.append(next_other)
        if details.tool is not None:
            if actionData.object_next_state == 'inhands':
                obj_data[details.target.id].state.holds = details.tool
            if actionData.object_next_state == 'not inhands':
                obj_data[details.target.id].state.holds = None
            if actionData.object_next_pos is not None:
                obj_data[details.tool.id].state.pos = actionData.object_next_pos
            if actionData.object_next_state is not None:
                obj_data[details.tool.id].state.state = actionData.object_next_state
            other = obj_data[details.tool.id].state.other
            next_other = actionData.object_followup
            if next_other is not None:
                if next_other.startswith('not'):
                    next_other_opposite = next_other.replace('not ','')
                elif next_other is not None:
                    next_other_opposite = f'not {next_other}'
                try:
                    other.remove(next_other_opposite)
                except ValueError:
                    pass
                other.append(next_other)



        msg: str = f'{details.author.id} {actionData.message_template}'.replace('<position>', obj_data[details.author.id].state.pos)
        if details.tool is not None:
            msg = msg.replace('<object>', details.tool.id)
        if details.target is not None:
            msg = msg.replace('<target>', details.target.id)

        print(msg)
        return actionData.effect

        

class ClownMoralSchema(AbsMoralSchema):
    def __init__(
        self,
        globals: GlobalDefs,
        perspective: Actor,
        feelings: InVec,
    ):
        self._globals = globals
        super().__init__(
            globals.space,
            globals.actors,
            Agency(perspective.id, feelings),
            globals.fabula,
        )
    
    @override
    def state(self) -> MsState:
        return MsState.Active

    @override
    def after_action(self) -> None:
        return

    @override
    def calc_likelihood(self, details: ActionDetails):
        if self._check_applicable(details):
            return details.action.data.prior
        return 0.0
    
    def _check_applicable(self, details: ActionDetails) -> bool:
        action: ActionData = details.action.data
        author = details.author
        target = details.target
        tool = details.tool
        if details.action.id == 'enters the room' and author.id == 'redhead':
            print(details)
        if not self._check_prerequisite(author, action.author):
            return False
        
        if not self._check_prerequisite(author, action.author_prerequisite):
            return False
        author_data: ObjectData = obj_data[author.id]
        if not self._check_state(action.author_state_before, author_data.state.state):
            return False
        if not self._check_pos(action.author_pos_before, author_data.state.pos):
            return False

        if not self._check_prerequisite(target, action.target):
            return False
        if not self._check_prerequisite(target, action.target_prerequisite):
            return False
        if target is not None:
            target_data: ObjectData = obj_data[target.id]
            if not self._check_state(action.target_state_before, target_data.state.state):
                return False
            if not self._check_pos(action.target_pos_before, target_data.state.pos):
                return False
        
        if not self._check_prerequisite(tool, action.object):
            return False
        if not self._check_prerequisite(tool, action.object_prerequisite):
            return False
        if tool is not None:
            tool_data: ObjectData = obj_data[tool.id]
            if not self._check_state(action.object_state_before, tool_data.state.state):
                return False
            if not self._check_pos(action.object_pos_before, tool_data.state.pos):
                return False
        return True
        
        
    def _check_prerequisite(self,
        obj: Object|None,
        prerequisite: str|None,
    ) -> bool:
        if prerequisite is None:
            return True
        if prerequisite == 'nothing':
            return obj is None
        elif obj is None:
            return False
        data: ObjectData = obj_data[obj.id]
        if prerequisite == 'holding':
            return data.state.holds is not None
        if prerequisite == 'not holding':
            return data.state.holds is None
        if prerequisite.startswith('not '):
            return prerequisite.split('not')[1] not in data.state.other
        if prerequisite in data.state.other:
            return True
        return (obj.id == prerequisite) or\
            (
                (prerequisite in object_groups.keys()) and\
                (obj in object_groups[prerequisite]) 
            ) or\
            (prerequisite in data.state.other)
    
    def _check_pos(self, needed: str|None, actual: str):
        if needed is None:
            return True
        if needed.startswith('not '):
            return needed.split('not')[1] != actual
        else:
            return needed == actual
        
    def _check_state(self, needed: str|None, actual: str):
        if needed is None:
            return True
        return needed == actual


globalDefs = GlobalDefs(0.1)

bica = Bica({
    a.id: [ClownMoralSchema(globalDefs, a, vec([0,0,0]))]
    for a in globalDefs.objects.values()
}, globalDefs)

def main():
    while bica.execute_action(lambda x: len({x.author, x.tool, x.target}) == 3 or (x.tool == None and x.target == None)) is not None:
        pass
    