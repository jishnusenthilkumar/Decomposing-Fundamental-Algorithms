from math import pi
from qiskit import QuantumCircuit, transpile
from .gates import RX, RY, RZ, CZ
from .euler import hadamard_as_native


def _to_native_gates(qc: QuantumCircuit):
    """Convert a Qiskit circuit to a list of native gates."""
    trans = transpile(qc, basis_gates=["rx", "ry", "rz", "cz"])
    gates = []
    for inst in trans.data:
        op, qargs, _ = inst
        qubits = [trans.qubits.index(q) for q in qargs]
        if op.name == "rx":
            gates.append(RX(qubits[0], float(op.params[0])))
        elif op.name == "ry":
            gates.append(RY(qubits[0], float(op.params[0])))
        elif op.name == "rz":
            gates.append(RZ(qubits[0], float(op.params[0])))
        elif op.name == "cz":
            gates.append(CZ(*qubits))
        else:
            raise ValueError(f"Unsupported gate type: {op.name}")
    return gates


def _multi_controlled_z(qubits: list[int]):
    """Return native gate list for a multi-controlled Z on ``qubits``."""
    if len(qubits) == 1:
        qc = QuantumCircuit(1)
        qc.rz(pi, 0)
        return _to_native_gates(qc)

    ctrl = qubits[:-1]
    tgt = qubits[-1]
    qc = QuantumCircuit(len(qubits))
    qc.mcp(pi, ctrl, tgt)
    return _to_native_gates(qc)


def diffusion(n: int):
    """Return native gate list implementing Grover's diffusion on ``n`` qubits."""
    gates = []
    for j in range(n):
        gates += hadamard_as_native(j)
    for j in range(n):
        gates.append(RX(j, pi))

    gates += _multi_controlled_z(list(range(n)))

    for j in range(n):
        gates.append(RX(j, pi))
    for j in range(n):
        gates += hadamard_as_native(j)
    return gates
