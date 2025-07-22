"""Utility decompositions for CP and SWAP using only native gates."""

from math import pi

from .gates import RX, RY, RZ, CZ


def _cnot_via_cz(ctrl: int, tgt: int):
    """Return gate list for a CX using CZ and single-qubit rotations."""
    return [
        RY(tgt, pi / 2),
        RX(tgt, pi),
        CZ(ctrl, tgt),
        RY(tgt, pi / 2),
        RX(tgt, pi),
    ]


def cp_via_cz(ctrl: int, tgt: int, theta: float):
    """Return gate list implementing ``CP(theta)`` using CZ gates."""

    gates = [RZ(ctrl, theta / 2)]
    gates += _cnot_via_cz(ctrl, tgt)
    gates.append(RZ(tgt, -theta / 2))
    gates += _cnot_via_cz(ctrl, tgt)
    gates.append(RZ(tgt, theta / 2))
    return gates


def swap_via_cz(a: int, b: int):
    """Return gate list implementing ``SWAP(a, b)`` using CZ gates."""

    gates = []
    gates += _cnot_via_cz(a, b)
    gates += _cnot_via_cz(b, a)
    gates += _cnot_via_cz(a, b)
    return gates
