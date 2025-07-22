from qiskit.quantum_info import Operator

from .. import qft, to_qiskit


def test_qft_produces_circuit(n):
    
    gates = qft(n)
    circuit = to_qiskit(gates, n)
    assert circuit.num_qubits == n
    assert len(gates) > 0
    # ensure resulting unitary is unitary by verifying Operator can be built
    Operator(circuit)
    print(circuit.draw()) # This will display the circuit if run in an interactive environment

test_qft_produces_circuit(4)