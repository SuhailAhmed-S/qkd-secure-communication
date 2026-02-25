"""
Module 3: Quantum Channel Module (Qiskit Aer Simulation)
Simulates qubit transmission from Alice to Bob through a quantum channel.
Handles optional Eve interception transparently.
"""

import random


def quantum_channel_transmit(alice_bits: list, alice_bases: list,
                              eve_enabled: bool = False) -> dict:
    """
    Simulates the quantum channel. If Eve is enabled, she intercepts first.

    In Qiskit this would be:
        - Build a QuantumCircuit per qubit
        - Apply Alice's encoding gates
        - Optionally let Eve measure and re-encode
        - Let Bob measure in his chosen basis
    Here we simulate the statistical outcome directly.

    Returns the bits as they arrive at Bob (possibly disturbed by Eve).
    """
    if eve_enabled:
        from eve import eve_intercept
        intercepted = eve_intercept(alice_bits, alice_bases)
        return {
            'transmitted_bits':  intercepted['resent_bits'],
            'transmitted_bases': intercepted['resent_bases'],
            'eve_active':        True,
            'eve_bases':         intercepted['eve_bases']
        }
    else:
        return {
            'transmitted_bits':  alice_bits[:],
            'transmitted_bases': alice_bases[:],
            'eve_active':        False,
            'eve_bases':         []
        }
