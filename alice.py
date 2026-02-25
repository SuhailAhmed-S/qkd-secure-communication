"""
Module 2: Alice Module (Quantum State Preparation)
Simulates the sender generating random bits encoded into quantum states.
Uses the BB84 protocol: bases (+) rectilinear and (×) diagonal.
"""

import random


def alice_prepare(num_qubits: int) -> dict:
    """
    Alice generates random bits and bases, then 'encodes' each bit
    as a quantum state description (simulating Qiskit circuit logic).

    BB84 encoding rules:
        Basis +  (rectilinear): bit 0 → |0⟩, bit 1 → |1⟩
        Basis ×  (diagonal):    bit 0 → |+⟩, bit 1 → |−⟩

    Gate representation (as in Qiskit):
        bit=1        → apply X gate (flip)
        basis=×      → apply H gate (Hadamard)
    """
    bits   = [random.randint(0, 1) for _ in range(num_qubits)]
    bases  = [random.choice(['+', '×']) for _ in range(num_qubits)]
    states = []  # human-readable quantum state labels

    for bit, basis in zip(bits, bases):
        if basis == '+':
            state = '|0⟩' if bit == 0 else '|1⟩'
        else:  # diagonal basis
            state = '|+⟩' if bit == 0 else '|−⟩'
        states.append(state)

    return {
        'bits':   bits,
        'bases':  bases,
        'states': states
    }
