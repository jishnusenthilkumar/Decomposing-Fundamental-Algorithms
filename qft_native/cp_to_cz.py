from qiskit import QuantumCircuit, transpile
from .gates import RX, RY, RZ, CZ


def cp_via_cz(ctrl, tgt, theta):
    """Return native gate list for controlled-phase e^{i theta |11><11|}."""
    n = max(ctrl, tgt) + 1
    qc = QuantumCircuit(n)
    qc.cp(theta, ctrl, tgt)
    tc = transpile(
        qc,
        basis_gates=["rx", "ry", "rz", "cz"],
        optimization_level=0,
    )

    gates = []
    for inst in tc.data:
        name = inst.operation.name
        qargs = [tc.find_bit(q).index for q in inst.qubits]
        params = inst.operation.params
        if name == "rx":
            gates.append(RX(qargs[0], params[0]))
        elif name == "ry":
            gates.append(RY(qargs[0], params[0]))
        elif name == "rz":
            gates.append(RZ(qargs[0], params[0]))
        elif name == "cz":
            gates.append(CZ(*qargs))
    return gates


def swap_via_cz(a, b):
    """Return native gate list implementing a SWAP between qubits ``a`` and
    ``b`` using CZs."""
    n = max(a, b) + 1
    qc = QuantumCircuit(n)
    qc.swap(a, b)
    tc = transpile(
        qc,
        basis_gates=["rx", "ry", "rz", "cz"],
        optimization_level=0,
    )
    gates = []
    for inst in tc.data:
        name = inst.operation.name
        qargs = [tc.find_bit(q).index for q in inst.qubits]
        params = inst.operation.params
        if name == "rx":
            gates.append(RX(qargs[0], params[0]))
        elif name == "ry":
            gates.append(RY(qargs[0], params[0]))
        elif name == "rz":
            gates.append(RZ(qargs[0], params[0]))
        elif name == "cz":
            gates.append(CZ(*qargs))
    return gates
