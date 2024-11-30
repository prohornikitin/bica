from dataclasses import dataclass
from math import sqrt
from typing import Optional, Self, TypeAlias


IntentionalityAxis: TypeAlias = str


@dataclass
class InSpace:
    axes: list[IntentionalityAxis]

    def __eq__(self, other):
        return self.axes == other.axes
    
    def __repr__(self):
        return repr(self.axes)

class InVec:
    _by_name: dict[str, float]
    space: InSpace

    def __init__(self, space: InSpace, data: list[float] = []):
        self.space = space
        if len(data) == 0:
            self._by_name = dict.fromkeys(space.axes, 0)
        elif not isinstance(data[-1], int) and not isinstance(data[-1], float):
            raise Exception(f'da {data}')
        else:
            self._by_name = dict()
            for k, v in zip(space.axes, data):
                self._by_name[k] = v

    def __add__(self, b: Self):
        assert(self.space == b.space)
        result = []
        for k in self.space.axes:
            result.append(self._by_name[k] + b._by_name[k])
        return InVec(self.space, result)
    
    def __sub__(self, b: Self):
        assert(self.space == b.space)
        result = []
        for k in self.space.axes:
            result.append(self._by_name[k] - b._by_name[k])
        return InVec(self.space, result)

    def __mul__(self, b: float):
        result = []
        for k in self.space.axes:
            result.append(self._by_name[k] * b)
        return InVec(self.space, result)
    
    def __rmul__(self, b: float):
        return self * b
        
    def __getitem__(self, i: IntentionalityAxis):
        return self._by_name[i]
    
    def __setitem__(self, i: IntentionalityAxis, value: float):
        self._by_name[i] = value
    
    def project(self, new_space: InSpace):
        data = []
        for axis in new_space.axes:
            data.append(self[axis])
        return InVec(new_space, data)
    
    def unproject(self, old_unprojected: Self):
        old_space = old_unprojected.space
        data = []
        for axis in old_space.axes:
            if axis in self.space.axes:
                data.append(self[axis])
            else:
                data.append(old_unprojected[axis])
        return InVec(old_space, data)
    
    def norm(self) -> float:
        n = 0.0
        for v in self._by_name.values():
            n += v * v
        # print(self._by_name)
        return sqrt(n)
    
    def __iter__(self):
        return map(lambda x: self._by_name[x], self.space.axes)
    
    def copy(self):
        c = InVec(self.space)
        c._by_name = self._by_name.copy()
        return c
    
    def __repr__(self):
        return repr(self._by_name.values())
