from bica.intensions import InSpace, InVec


space = InSpace(
    'valence',
    'arousal',
    'dominance',
)


def vec(data: list[float] = []) -> InVec:
    return InVec(space, data)