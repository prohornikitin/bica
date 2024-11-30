from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional
from bica.base import Actor

from .intensions import vec
from bica.base import Object, ObjectId


rat =       Actor('rat', vec())
redhead =   Actor('Redhead', vec([-0.75, 0.5, 0]))
whiteface = Actor('Whiteface', vec([0.75, -0.5, 0]))
apple =     Actor('apple', vec([1, -0.5, 0]))
banana =    Actor('banana', vec([1, -0.5, 0]))
chair =     Actor('chair', vec([0.5, -0.5, -0.5]))
shotgun =   Actor('shotgun', vec([0, 1, 1]))
hammer =    Actor('hammer', vec([0, 1, 0.9]))
mirror =    Actor('mirror', vec([0.5, 0, 0]))
rake =      Actor('rake', vec([0, 0, 0]))
vodka =     Actor('vodka', vec([1, 1, 0]))
pepper =    Actor('pepper', vec([-1, 1, 0]))
trash =     Actor('trash', vec([0, 0, 0]))
bouquet_of_flowers = Actor('flowers', vec([1, -0.5, -1]))

allObjects = {apple, banana, chair, shotgun, hammer, mirror, rake, rat, vodka,pepper, trash, bouquet_of_flowers, rat, redhead, whiteface}

object_groups = {
    'agent': {redhead, whiteface},
    'actor': allObjects,
    'hangable': {shotgun, hammer, rake},
    'movable': {apple, banana, chair, shotgun, hammer, mirror, rake, rat, vodka, pepper, trash, bouquet_of_flowers},
    'offerable': {apple, banana, bouquet_of_flowers, shotgun, hammer, rat, vodka, pepper},
    'pickable': {apple, banana, bouquet_of_flowers, shotgun, hammer, rake, rat, vodka, pepper},
    'trashable': {apple, bouquet_of_flowers, shotgun, hammer, rake, rat, vodka, pepper},
}


@dataclass
class FullObjectState:
    state: str
    pos: str
    other: list[str]
    holds: ObjectId|None


@dataclass
class ObjectData:
    state: FullObjectState


obj_data = {
    rat.id: ObjectData(FullObjectState('alive', 'trash', [], None)),
    redhead.id: ObjectData(FullObjectState('away', 'standing', [], None)),
    whiteface.id: ObjectData(FullObjectState('present', 'standing', [], None)),
    apple.id: ObjectData(FullObjectState('whole', 'plate', [], None)),
    banana.id: ObjectData(FullObjectState('whole', 'plate', [], None)),
    chair.id: ObjectData(FullObjectState('intact', 'table', [], None)),
    shotgun.id: ObjectData(FullObjectState('loaded', 'hanging', [], None)),
    hammer.id: ObjectData(FullObjectState('hanger', 'hanging', [], None)),
    mirror.id: ObjectData(FullObjectState('direct', 'upright', [], None)),
    rake.id: ObjectData(FullObjectState('hanger', 'hanging', [], None)),
    vodka.id: ObjectData(FullObjectState('unopened', 'edge', [], None)),
    pepper.id: ObjectData(FullObjectState('in the pepperbox', 'table', [], None)),
    trash.id: ObjectData(FullObjectState('closed', 'place', [], None)),
    bouquet_of_flowers.id: ObjectData(FullObjectState('in the vase', 'floor', [], None)),
}