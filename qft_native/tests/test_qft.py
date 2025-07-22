from qiskit.quantum_info import Operator
from qft_native import qft, to_qiskit


def test_qft_produces_circuit():
    """Basic check that ``qft`` returns a valid circuit."""
    n = 4
    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    Operator(circuit)  # ensure circuit is unitary


if __name__ == "__main__":
    test_qft_produces_circuit()
