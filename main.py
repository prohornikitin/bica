from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

type Actor = Any # TODO:
type Role = str
type BindedSchema = Any # TODO:

@dataclass
class MoralSchema:
    interface: MoralSchemaInterface
    fabula: Fabula


@dataclass
class MoralSchemaInterface:
    roles: List[Role]
    tryBind: Callable[[List[Actor]], Optional[BindedSchema]]

@dataclass
class Fabula:
    pass

@dataclass
class Agency:
    #TODO: mood: 
    perspective: Role


@dataclass
class BindedSchema:
    fabula: Fabula
    actors: List[Role, Actor]

    