import math
from .gates import RX, RZ


def hadamard_as_native(q):
    """Decompose a Hadamard gate into native rotations."""
    return [
        RZ(q, math.pi / 2),
        RX(q, math.pi / 2),
        RZ(q, math.pi / 2),
    ]
