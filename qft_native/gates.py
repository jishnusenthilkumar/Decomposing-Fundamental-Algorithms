# qft_native/gates.py
from dataclasses import dataclass
@dataclass(frozen=True)
class Gate:
    name: str; qubits: tuple; params: tuple = ()
class RX(Gate):  def __init__(self,q,θ): super().__init__("RX",(q,), (θ,))
class RY(Gate):  def __init__(self,q,θ): super().__init__("RY",(q,), (θ,))
class RZ(Gate):  def __init__(self,q,θ): super().__init__("RZ",(q,), (θ,))
class CZ(Gate):  def __init__(self,ctrl,tgt): super().__init__("CZ",(ctrl,tgt))

# qft_native/euler.py
import math
def hadamard_as_native(q):
    return [RY(q, math.pi/2), RZ(q, math.pi), RY(q, math.pi/2)]

# qft_native/cp_to_cz.py
def cp_via_cz(ctrl, tgt, theta):
    """Return native gate list for controlled-phase e^{i θ |11⟩⟨11|}."""
    from .gates import CZ, RZ
    return [
        CZ(ctrl, tgt),
        RZ(tgt, -theta/2),
        CZ(ctrl, tgt),
        RZ(tgt,  theta/2),
    ]

# qft_native/qft.py
from math import pi
from .gates import *
from .euler import hadamard_as_native
from .cp_to_cz import cp_via_cz
def qft(n, *, do_swaps=True, adjoint=False, atol=1e-10):
    g=[]
    angles=[pi/2**k for k in range(1,n)]          # base angles
    qubits=range(n) if not adjoint else range(n-1,-1,-1)
    sign = -1 if adjoint else 1
    for j,qj in enumerate(qubits):
        g+=hadamard_as_native(qj)
        for k,θ in enumerate(angles[:n-j-1], start=1):
            ctrl = qj+k if not adjoint else qj-k
            g+=cp_via_cz(ctrl, qj, sign*θ)
    if do_swaps and not adjoint:
        for i in range(n//2):
            ctrl, tgt = i, n-1-i
            g+=cp_via_cz(ctrl,tgt,pi)            # H-CNOT-H swap via CZ (3×CZ)
            g+=cp_via_cz(tgt,ctrl,pi)
            g+=cp_via_cz(ctrl,tgt,pi)
    return g
