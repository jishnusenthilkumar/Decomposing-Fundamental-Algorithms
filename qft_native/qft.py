from math import pi
from .euler import hadamard_as_native
from .cp_to_cz import cp_via_cz, swap_via_cz


def qft(n, *, do_swaps=True, adjoint=False):
    """Return a list of native gates implementing the QFT on ``n`` qubits."""
    gates = []
    if adjoint:
        qubits = range(n)
        for j in qubits:
            # inverse order of forward circuit
            for k in range(j):
                angle = -pi / (2 ** (j - k))
                gates += cp_via_cz(j, k, angle)
            gates += hadamard_as_native(j)
        if do_swaps:
            for i in range(n // 2):
                ctrl, tgt = i, n - 1 - i
                gates += swap_via_cz(ctrl, tgt)
        return gates

    # forward QFT
    for j in reversed(range(n)):
        for k in reversed(range(j)):
            angle = pi * (2 ** (k - j))
            gates += cp_via_cz(k, j, angle)
        gates += hadamard_as_native(j)

    if do_swaps:
        for i in range(n // 2):
            ctrl, tgt = i, n - 1 - i
            gates += swap_via_cz(ctrl, tgt)
    return gates
