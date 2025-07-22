from qiskit.quantum_info import Operator
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from grover_native.grover import diffusion
from grover_native.simulator import to_qiskit


def test_diffusion_produces_circuit(n: int = 3):
    """Basic check that ``diffusion`` returns a valid circuit."""
    gates = diffusion(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    Operator(circuit)  # ensure circuit is unitary
    print(circuit.draw())


if __name__ == "__main__":
    test_diffusion_produces_circuit()
