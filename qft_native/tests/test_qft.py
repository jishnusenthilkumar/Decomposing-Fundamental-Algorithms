import os
import sys
from qiskit.quantum_info import Operator

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    ),
)  # noqa: E402

from qft_native import qft, to_qiskit  # noqa: E402


def test_qft_produces_circuit(n):

    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    # ensure resulting unitary is unitary by verifying Operator can be built
    Operator(circuit)
    # This will display the circuit if run in an interactive environment
    print(circuit.draw())


test_qft_produces_circuit(4)
