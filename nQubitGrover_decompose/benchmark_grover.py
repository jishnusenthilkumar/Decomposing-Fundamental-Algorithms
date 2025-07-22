import argparse
import time

from qiskit import QuantumCircuit, transpile

import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from grover_native.grover import diffusion
from grover_native.simulator import to_qiskit


def build_native_circuit(num_qubits: int) -> QuantumCircuit:
    """Return the native Grover diffusion circuit."""
    gates = diffusion(num_qubits)
    return to_qiskit(gates, num_qubits)


def build_standard_circuit(num_qubits: int) -> QuantumCircuit:
    """Return a standard Grover diffusion circuit transpiled to native basis."""
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
    return transpile(qc, basis_gates=["rx", "ry", "rz", "cz"])


def benchmark(num_qubits: int) -> None:
    start = time.perf_counter()
    native = build_native_circuit(num_qubits)
    native_time = time.perf_counter() - start

    start = time.perf_counter()
    transpiled = build_standard_circuit(num_qubits)
    transpile_time = time.perf_counter() - start

    native_counts = native.count_ops()
    transpiled_counts = transpiled.count_ops()

    print(f"Native circuit gate counts: {native_counts}")
    print(f"Standard circuit gate counts: {transpiled_counts}")
    print(f"Native circuit build time: {native_time:.6f} s")
    print(f"Standard transpile time: {transpile_time:.6f} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark native vs standard Grover diffusion")
    parser.add_argument("n", type=int, nargs="?", default=3, help="Number of qubits")
    args = parser.parse_args()
    benchmark(args.n)
