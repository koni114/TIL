from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType()
