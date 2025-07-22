from math import pi

from .euler import hadamard_as_native
from .cp_to_cz import cp_via_cz
from .qft import qft


def qpe(num_ancilla: int, theta: float):
    """Return a list of native gates implementing QPE for RZ(theta).

    The algorithm estimates the phase of ``RZ(theta)`` given the eigenstate
    ``|1>`` on the target qubit. ``num_ancilla`` specifies the number of
    ancilla qubits used for phase estimation.
    """
    gates = []
    # Apply Hadamard to ancilla qubits
    for j in range(num_ancilla):
        gates += hadamard_as_native(j)

    target = num_ancilla

    # Apply controlled RZ^{2^k}
    for k in range(num_ancilla):
        angle = theta * (2 ** k)
        gates += cp_via_cz(k, target, angle)

    # Inverse QFT on ancilla qubits without swaps
    gates += qft(num_ancilla, do_swaps=False, adjoint=True)
    return gates
