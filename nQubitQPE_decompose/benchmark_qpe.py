import argparse
import time

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT

import os
import sys

# Ensure the "qpe_native" package inside ``nQubitQPE_decompose`` is importable
PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from qpe_native.qpe import qpe
from qpe_native.simulator import to_qiskit


def build_native_circuit(num_ancilla: int, theta: float) -> QuantumCircuit:
    """Return the native QPE circuit."""
    gates = qpe(num_ancilla, theta)
    return to_qiskit(gates, num_ancilla + 1)


def build_standard_circuit(num_ancilla: int, theta: float) -> QuantumCircuit:
    """Return a standard QPE circuit transpiled to native basis gates."""
    qc = QuantumCircuit(num_ancilla + 1)
    for j in range(num_ancilla):
        qc.h(j)
    for j in range(num_ancilla):
        qc.cp(theta * (2 ** j), j, num_ancilla)
    qft = QFT(num_ancilla, do_swaps=False, inverse=True)
    qc.append(qft.to_instruction(), range(num_ancilla))
    return transpile(qc, basis_gates=["rx", "ry", "rz", "cz"])


def benchmark(num_ancilla: int, theta: float) -> None:
    start = time.perf_counter()
    native_circuit = build_native_circuit(num_ancilla, theta)
    native_time = time.perf_counter() - start

    start = time.perf_counter()
    transpiled = build_standard_circuit(num_ancilla, theta)
    transpile_time = time.perf_counter() - start

    native_counts = native_circuit.count_ops()
    transpiled_counts = transpiled.count_ops()

    print(f"Native circuit gate counts: {native_counts}")
    print(f"Standard circuit gate counts: {transpiled_counts}")
    print(f"Native circuit build time: {native_time:.6f} s")
    print(f"Standard transpile time: {transpile_time:.6f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark native vs standard QPE")
    parser.add_argument("n", type=int, nargs="?", default=3, help="Number of ancilla qubits")
    parser.add_argument("theta", type=float, nargs="?", default=3.14159 / 2, help="Phase angle")
    args = parser.parse_args()
    benchmark(args.n, args.theta)
