import os
import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from qft_native.cp_to_cz import cp_via_cz, swap_via_cz
from qft_native.reverse import reverse_circuit
from qft_native.simulator import to_qiskit
from qft_native.gates import RX, RY, CZ


def unitaries_equal_up_to_global_phase(u1, u2, tol=1e-7):
    """Return True if unitary matrices are equal up to global phase."""
    diff = u1 @ u2.conj().T
    phase = diff[0, 0]
    return np.allclose(diff / phase, np.eye(u1.shape[0]), atol=tol)


def test_cp_via_cz_equivalent_to_qiskit():
    theta = 0.3
    gates = cp_via_cz(0, 1, theta)
    custom = to_qiskit(gates, 2)

    reference = QuantumCircuit(2)
    reference.cp(theta, 0, 1)

    assert unitaries_equal_up_to_global_phase(
        Operator(custom).data, Operator(reference).data
    )


def test_swap_via_cz_equivalent_to_qiskit():
    gates = swap_via_cz(0, 1)
    custom = to_qiskit(gates, 2)

    reference = QuantumCircuit(2)
    reference.swap(0, 1)

    assert unitaries_equal_up_to_global_phase(
        Operator(custom).data, Operator(reference).data
    )


def test_reverse_circuit_produces_adjoint():
    gates = [RX(0, 0.2), RY(1, -0.3), CZ(0, 1)]
    qc = to_qiskit(gates, 2)

    reversed_qc = to_qiskit(reverse_circuit(gates), 2)

    assert unitaries_equal_up_to_global_phase(
        Operator(reversed_qc).data, Operator(qc).adjoint().data
    )
