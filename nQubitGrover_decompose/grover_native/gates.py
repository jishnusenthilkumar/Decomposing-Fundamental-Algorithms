from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    """Representation of a native gate."""
    name: str
    qubits: tuple
    params: tuple = ()


class RX(Gate):
    def __init__(self, q, theta):
        super().__init__("RX", (q,), (theta,))


class RY(Gate):
    def __init__(self, q, theta):
        super().__init__("RY", (q,), (theta,))


class RZ(Gate):
    def __init__(self, q, theta):
        super().__init__("RZ", (q,), (theta,))


class CZ(Gate):
    def __init__(self, ctrl, tgt):
        super().__init__("CZ", (ctrl, tgt))
