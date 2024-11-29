from dataclasses import dataclass
from enum import Enum
from typing import Optional
from bica.base import Action, ActionEffect, ActorId
from .base import vec





# Agent = ''

# Hangeable = {Object.Shotgun, Object.Hammer, Object.Rake}
# Movable = set(Object).difference() 


# @dataclass
# class Holding:
#     what: Any

type S = State
type Effect = ActionEffect


@dataclass
class ActionData:
    effect: ActionEffect
    required_state: list[State]
    required_author: Optional[ActorId] = None


Action('fall',        ActionData(Effect(vec(), vec(), 0, 0), [S.OnEdge])),
Action('rat-run',     ActionData(Effect(vec(), vec(), 0, 0), [S.Present, S.NotInTrash])),
Action('drop',        ActionData(Effect(vec(-1,-1,-1), vec(), 0.1, 0), [S.Present, S.Standing])),
Action('rip',         ActionData(Effect(vec(-0.7, 0.7, 0.9), vec(), 0.1, 0), [S.Present, S.Standing])),
Action('is-shot',     ActionData(Effect(vec(), vec(), 0, 0), [S.Present, S.NotInTrash])),
Action('take',        ActionData(Effect(vec(1,1,1), vec(), 0.1, 0), [S.Present, S.Standing, S.NotHolding])),
Action('walkto',      ActionData(Effect(vec(), vec(), 0, 0), [S.Present, S.NotInTrash, S.Called])),
Action('banana-peel', ActionData(Effect(vec(0.5, -1, 1, -1), vec(), 0, 0))),
Action('chandelier',  ActionData(Effect(vec(0.3, -0.4, 0.5, -0.3), vec(), 0, 0), [S.Present, S.Standing])),
Action('gun-step',    ActionData(Effect(vec(), vec(), ))),
Action('hammer-st'),
Action('notice'),
Action('rake-step'),
Action('vodka-st'),
Action('beg'),
Action('chase'),
Action('expel'),
Action('fight'),
Action('fist'),
Action('flee'),
Action('greet'),
Action('ignore'),
Action('kick'),
Action('mid-finger'),
Action('nose'),
Action('pat'),
Action('point'),
Action('ruffle'),
Action('slap'),
Action('trash'),
Action('accept'),
Action('decline'),
Action('greet-ignore'),
Action('greet-respect'),
Action('brush'),
Action('enter'),
Action('intotrash'),
Action('jump'),
Action('leave'),
Action('outoftrash'),
Action('ruffle-self'),
Action('walking'),
Action('putright'),
Action('putwrong'),
Action('set-flowers'),
Action('flip-flowers'),
Action('load-gun'),
Action('close-trash'),
Action('open-trash'),
Action('break-chair'),
Action('break-rake'),
Action('hammer-mir'),
Action('hammer-rat'),
Action('rake-pepper'),
Action('shoot-mirror'),
Action('shoot-rat'),
Action('hammer'),
Action('offer'),
Action('shoot-other'),
Action('sprinkle'),
Action('eat-apple'),
Action('eat-banana'),
Action('mirror-funny'),
Action('mirror-smart'),
Action('pepper'),
Action('rise'),
Action('shoot-self'),
Action('shotgun'),
Action('sit'),
Action('vodka'),
Action('attack'),
Action('backaway'),
Action('