from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from .gates import RX, RY, RZ, CZ


def to_qiskit(gates, n):
    """Convert a list of native gates into a Qiskit ``QuantumCircuit``."""
    qc = QuantumCircuit(n)
    for g in gates:
        if isinstance(g, RX):
            qc.rx(g.params[0], g.qubits[0])
        elif isinstance(g, RY):
            qc.ry(g.params[0], g.qubits[0])
        elif isinstance(g, RZ):
            qc.rz(g.params[0], g.qubits[0])
        elif isinstance(g, CZ):
            qc.cz(*g.qubits)
        else:
            raise ValueError(f"Unsupported gate type: {g}")
    return qc


def unitary(gates, n):
    """Return the unitary matrix for the given native gate sequence."""
    qc = to_qiskit(gates, n)
    return Operator(qc).data
