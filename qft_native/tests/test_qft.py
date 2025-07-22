from qiskit.quantum_info import Operator
from qft_native import qft, to_qiskit  # Adjust if your module is elsewhere

def test_qft_produces_circuit(n):
    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    Operator(circuit)  # checks if circuit is unitary
    print(circuit.draw())

if __name__ == "__main__":
    test_qft_produces_circuit(4)
