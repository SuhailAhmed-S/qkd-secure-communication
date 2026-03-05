"""
Module 3: Quantum Channel Module

Simulates the quantum channel through which qubits travel from Alice to Bob.
Handles optional eavesdropping (Eve interception) transparently.

Description:
    The quantum channel is the medium through which Alice sends her encoded
    qubits to Bob. This module simulates:
    
    1. Clean Channel (no eavesdropping):
       Alice's qubits travel directly to Bob with no disturbance
       
    2. Compromised Channel (with Eve):
       Eve intercepts the quantum bits, measures them, and resends
       This introduces detectable errors (elevated QBER)
    
    Real Implementation (Qiskit):
        In a real quantum system using Qiskit, this would involve:
        - Creating QuantumCircuits for each qubit
        - Applying encoding gates based on Alice's bases and bits
        - Applying optional Eve measurement and re-encoding
        - Transmitting through a quantum channel simulator
        - Allowing Bob to measure in his chosen bases
    
    This module simulates the statistical outcomes directly without
    explicit quantum circuit construction.
"""

from typing import Dict, List


def quantum_channel_transmit(alice_bits: List[int], alice_bases: List[str],
                              eve_enabled: bool = False) -> Dict[str, object]:
    """
    Simulates quantum channel transmission from Alice to Bob.
    
    If eavesdropping is enabled, Eve intercepts and measures the qubits,
    introducing detectable disturbances. Otherwise, qubits are transmitted
    cleanly.
    
    Args:
        alice_bits (List[int]): Alice's encoded bits
        alice_bases (List[str]): Alice's encoding bases
        eve_enabled (bool): Whether Eve should intercept and resend.
                          Default: False (clean channel)
                          
    Returns:
        Dict[str, object]: Dictionary containing:
            - 'transmitted_bits': List[int] - Bits arriving at Bob
            - 'transmitted_bases': List[str] - Bases encoding those bits
            - 'eve_active': bool - Whether Eve was active
            - 'eve_bases': List[str] - Eve's measurement bases (empty if no Eve)
            
    Note:
        When Eve is inactive, the transmitted bits and bases are identical
        to Alice's originals (transparent channel).
        
        When Eve is active, the transmitted bits/bases are Eve's resent values,
        which differ from Alice's due to measurement errors when Eve's basis
        didn't match Alice's.
        
    Qiskit Analogy:
        In a real Qiskit implementation, this would be:
        ```
        qc = QuantumCircuit(1)
        if bit == 1:
            qc.x(0)  # Apply X gate for bit=1
        if basis == '×':
            qc.h(0)  # Apply H gate for diagonal basis
        # optionally measure for Eve
        if eve_enabled:
            qc.measure(0, classical_bit)
        # Bob measures in his basis
        ```
    """
    if eve_enabled:
        # Eve intercepts the quantum bits
        from eve import eve_intercept
        
        intercepted = eve_intercept(alice_bits, alice_bases)
        return {
            'transmitted_bits': intercepted['resent_bits'],
            'transmitted_bases': intercepted['resent_bases'],
            'eve_active': True,
            'eve_bases': intercepted['eve_bases']
        }
    else:
        # Clean channel: qubits transmitted without disturbance
        return {
            'transmitted_bits': alice_bits[:],  # Copy to avoid aliasing
            'transmitted_bases': alice_bases[:],
            'eve_active': False,
            'eve_bases': []
        }
