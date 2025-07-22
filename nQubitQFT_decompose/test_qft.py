from qiskit.quantum_info import Operator
from qft_native.qft import qft
from qft_native.simulator import to_qiskit


def test_qft_produces_circuit(n):
    """Basic check that ``qft`` returns a valid circuit."""
    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    Operator(circuit)  # ensure circuit is unitary
    print(circuit.draw())


if __name__ == "__main__":
    test_qft_produces_circuit(3)
