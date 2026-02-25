"""
Module 4: Eve Module (Attack Simulation — Intercept-Resend Attack)
Eve randomly selects measurement bases, measures qubits, and resends.
This introduces ~25% errors in the sifted key (detectable via QBER).

BB84 measurement rules:
    If Eve's basis matches Alice's basis → correct bit measured
    If Eve's basis differs              → random bit (50% chance of error)
    Eve then re-encodes and resends her measured result.
"""

import random


def eve_intercept(alice_bits: list, alice_bases: list) -> dict:
    """
    Simulates Eve's intercept-resend attack.
    Returns the bits and bases that Eve resends to Bob.
    """
    num_qubits   = len(alice_bits)
    eve_bases    = [random.choice(['+', '×']) for _ in range(num_qubits)]
    resent_bits  = []
    resent_bases = []

    for i in range(num_qubits):
        if eve_bases[i] == alice_bases[i]:
            # Correct basis → Eve gets the right bit
            measured_bit = alice_bits[i]
        else:
            # Wrong basis → Eve gets a random result (superposition collapse)
            measured_bit = random.randint(0, 1)

        resent_bits.append(measured_bit)
        resent_bases.append(eve_bases[i])   # Eve resends in her (random) basis

    return {
        'eve_bases':    eve_bases,
        'resent_bits':  resent_bits,
        'resent_bases': resent_bases
    }
