from typing import Iterable
from .gates import Gate


def reverse_circuit(gates: Iterable[Gate]):
    """Return the reversed list of gates with each gate adjointed."""
    rev = []
    for g in reversed(list(gates)):
        if g.name in {"RX", "RY", "RZ"}:
            theta = -g.params[0]
            cls = type(g)
            rev.append(cls(g.qubits[0], theta))
        elif g.name == "CZ":
            rev.append(g)  # self-adjoint
        else:
            raise ValueError(f"Unsupported gate: {g}")
    return rev
