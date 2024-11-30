from dataclasses import dataclass
from pathlib import Path

import numpy as np
from bica.base import Action, ActionEffect
from .intensions import vec
# from openpyxl import load_workbook, Workbook, Worksheet
import pandas as pd




@dataclass(unsafe_hash=True)
class ActionData:
    effect: ActionEffect
    message_template: str
    prior: float
    
    author: str
    author_state_before: str|None
    author_pos_before:   str|None
    author_prerequisite: str|None
    author_next_state: str|None
    author_next_pos:   str|None
    author_followup: str|None

    object: str
    object_state_before: str|None
    object_pos_before:   str|None
    object_prerequisite: str|None
    object_next_state: str|None
    object_next_pos:   str|None
    object_followup: str|None

    target: str
    target_state_before: str|None
    target_pos_before:   str|None
    target_prerequisite: str|None
    target_next_state: str|None
    target_next_pos:   str|None
    target_followup: str|None
    

def parse_action(data: pd.Series) -> Action:
    id = data['name'] 
    effect = ActionEffect(
        vec(list(map(float, [data['v1'], data['a1'], data['d1']]))),
        vec(list(map(float, [data['v2'], data['a2'], data['d2']]))),
        float(data['w1']),
        float(data['w2']),
    )

    actionData = ActionData(
        effect,
        data['message'],
        float(data['prior']),
        
        data['author'] or 'agent',
        data['astate1'],
        data['apos1'],
        data['apre'],
        data['astate2'],
        data['apos2'],
        data['apost'],

        data['object'] or 'nothing',
        data['ostate1'],
        data['opos1'],
        data['opre'],
        data['ostate2'],
        data['opos2'],
        data['opost'],

        data['target'] or 'nothing',
        data['tstate1'],
        data['tpos1'],
        data['tpre'],
        data['tstate2'],
        data['tpos2'],
        data['tpost'],
    )
    return Action(
        id,
        actionData
    )


excel = pd.read_excel(
    Path(__file__).parent / 'schema.xlsx', header=3, dtype=str
)
actions = list(map(lambda x: parse_action(x[1]), excel.replace(np.nan, None).iterrows()))