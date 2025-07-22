from qiskit.quantum_info import Operator
from math import pi
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from qpe_native.qpe import qpe
from qpe_native.simulator import to_qiskit


def test_qpe_produces_circuit(n: int = 3):
    """Basic check that ``qpe`` returns a valid circuit."""
    theta = pi / 2
    gates = qpe(n, theta)
    circuit = to_qiskit(gates, n + 1)
    assert circuit.num_qubits == n + 1
    assert len(gates) > 0
    Operator(circuit)  # ensure circuit is unitary
    print(circuit.draw())


if __name__ == "__main__":
    test_qpe_produces_circuit()
