import argparse
import time

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT

import os
import sys

# Ensure the "qft_native" package inside ``nQubitQFT_decompose`` is importable
PROJECT_ROOT = os.path.dirname(__file__)
PACKAGE_PATH = os.path.join(PROJECT_ROOT, "nQubitQFT_decompose")
if PACKAGE_PATH not in sys.path:
    sys.path.insert(0, PACKAGE_PATH)

from qft_native.qft import qft
from qft_native.simulator import to_qiskit


def build_native_circuit(num_qubits: int) -> QuantumCircuit:
    """Return the native QFT circuit for ``num_qubits`` qubits."""
    gates = qft(num_qubits)
    return to_qiskit(gates, num_qubits)


def build_transpiled_circuit(num_qubits: int) -> QuantumCircuit:
    """Return the standard QFT circuit transpiled to native basis gates."""
    qft_circuit = QFT(num_qubits)
    return transpile(qft_circuit, basis_gates=["rx", "ry", "rz", "cz"])


def benchmark(num_qubits: int) -> None:
    start = time.perf_counter()
    native_circuit = build_native_circuit(num_qubits)
    native_time = time.perf_counter() - start

    start = time.perf_counter()
    transpiled = build_transpiled_circuit(num_qubits)
    transpile_time = time.perf_counter() - start

    native_counts = native_circuit.count_ops()
    transpiled_counts = transpiled.count_ops()

    print(f"Native circuit gate counts: {native_counts}")
    print(f"Transpiled circuit gate counts: {transpiled_counts}")
    print(f"Native circuit build time: {native_time:.6f} s")
    print(f"Transpile time: {transpile_time:.6f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark native vs transpiled QFT")
    parser.add_argument("n", type=int, nargs="?", default=3, help="Number of qubits")
    args = parser.parse_args()
    benchmark(args.n)