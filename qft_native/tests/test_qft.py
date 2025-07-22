import os
import sys
from qiskit.quantum_info import Operator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from qft_native import qft, to_qiskit


def test_qft_produces_circuit():
    n = 3
    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    # ensure resulting unitary is unitary by verifying Operator can be built
    Operator(circuit)
