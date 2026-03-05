"""
Module 2: Alice Module (Quantum State Preparation)

Simulates the sender generating random bits encoded into quantum states.
Uses the BB84 protocol: bases (+) rectilinear and (×) diagonal.

Description:
    Alice prepares qubits by:
    1. Generating random bits (0 or 1)
    2. Selecting random measurement bases (+ or ×)
    3. Encoding bits as quantum states according to BB84 rules

BB84 Encoding Rules:
    Rectilinear Basis (+):
        - Bit 0 → |0⟩ (horizontal polarization)
        - Bit 1 → |1⟩ (vertical polarization)
    
    Diagonal Basis (×):
        - Bit 0 → |+⟩ (45° polarization)
        - Bit 1 → |−⟩ (135° polarization)

Quantum Gate Representation (Qiskit analogy):
    - Bit 1: Apply X gate (Pauli-X, bit-flip operation)
    - Diagonal basis: Apply H gate (Hadamard, basis rotation)
"""

import random
from typing import Dict, List


def alice_prepare(num_qubits: int) -> Dict[str, List]:
    """
    Alice generates random bits and measurement bases, then encodes each bit
    as a quantum state description.
    
    This simulates the initial step of the BB84 quantum key distribution protocol.
    Alice's choices are completely random and remain secret until basis 
    reconciliation occurs over the classical channel.
    
    Args:
        num_qubits (int): Number of qubits to prepare. Should be >= 10.
        
    Returns:
        Dict[str, List]: Dictionary containing:
            - 'bits': List[int] - Random bits (0 or 1) for each qubit
            - 'bases': List[str] - Random bases ('+' or '×') for each qubit
            - 'states': List[str] - Human-readable quantum state labels
            
    Raises:
        ValueError: If num_qubits is less than 1
        
    Example:
        >>> data = alice_prepare(5)
        >>> len(data['bits']) == len(data['bases']) == len(data['states']) == 5
        True
    """
    # Input validation
    if not isinstance(num_qubits, int) or num_qubits < 1:
        raise ValueError(f"num_qubits must be a positive integer, got {num_qubits}")
    
    # Generate random bits and bases
    bits: List[int] = [random.randint(0, 1) for _ in range(num_qubits)]
    bases: List[str] = [random.choice(['+', '×']) for _ in range(num_qubits)]
    states: List[str] = []

    # Encode bits as quantum state descriptions
    for bit, basis in zip(bits, bases):
        if basis == '+':
            # Rectilinear basis
            state = '|0⟩' if bit == 0 else '|1⟩'
        else:
            # Diagonal basis (basis == '×')
            state = '|+⟩' if bit == 0 else '|−⟩'
        states.append(state)

    return {
        'bits': bits,
        'bases': bases,
        'states': states
    }
