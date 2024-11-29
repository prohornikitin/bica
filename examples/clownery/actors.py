from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional
from bica.base import Actor

from .base import vec
from bica.base import Object, ObjectId


Rat =       Actor('Rat', vec())
Redhead =   Actor('Redhead', vec(-0.75, 0.5, 0))
Whiteface = Actor('Whiteface', vec(0.75, -0.5, 0))
Apple =   Object('Apple', vec(1, -0.5, 0))
Banana =  Object('Banana', vec(1, -0.5, 0))
Chair =   Object('Chair', vec(0.5, -0.5, -0.5))
Shotgun = Object('Shotgun', vec(0, 1, 1))
Hammer =  Object('hammer', vec(0, 1, 0.9))
Mirror =  Object('Mirror', vec(0.5, 0, 0))
Rake =    Object('Rake', vec(0, 0, 0))
Vodka =   Object('Vodka', vec(1, 1, 0))
Pepper =  Object('Pepper', vec(-1, 1, 0))
Trash =   Object('Trash', vec(0, 0, 0))
BouquetOfFlowers = Object('BouquetOfFlowers', vec(1, -0.5, -1))

AllObjects = {Apple, Banana, Chair, Shotgun, Hammer, Mirror, Rake, Rat, Vodka, Pepper, Trash, BouquetOfFlowers, Rat, Redhead, Whiteface} 

# Actors = {Rat, Redhead, Whiteface}
Hangable = {Shotgun, Hammer, Rake}
Movable = {Apple, Banana, Chair, Shotgun, Hammer, Mirror, Rake, Rat, Vodka, Pepper, Trash, BouquetOfFlowers}
Offerable = {Apple, Banana, BouquetOfFlowers, Shotgun, Hammer, Rat, Vodka, Pepper}
Pickable = {Apple, Banana, BouquetOfFlowers, Shotgun, Hammer, Rake, Rat, Vodka, Pepper}
Trashable = {Apple, BouquetOfFlowers, Shotgun, Hammer, Rake, Rat, Vodka, Pepper}


class State2(StrEnum):
    NotResponded = auto()
    Called = auto()


class Location(StrEnum):
    OnTableEdge = auto()
    InTrash = auto()
    Floor = auto()
    Away = auto()


class Position(StrEnum):
    Standing = auto()
    Sitting = auto()


@dataclass
class ObjectState:
    location: Location

class ActorState(ObjectState):
    position: Position
    inHands: Optional[Object]
    state2: State2

    def __init__(self, location: Location, position: Position, inHands: Optional[Object] = None):
        super().__init__(location)
        self.inHands = inHands
        self.position = position


state = dict[ObjectId, ActorState]