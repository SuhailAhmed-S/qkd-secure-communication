"""
Module 5: Bob Module & Key Sifting
Bob measures received qubits in randomly chosen bases, then compares
with Alice to keep only bits where their bases matched (sifted key).

BB84 measurement:
    If Bob's basis == Alice's (or Eve's) basis → correct result
    If Bob's basis ≠ transmitted basis         → random result
"""

import random


def bob_measure(transmitted_bits: list, transmitted_bases: list) -> dict:
    """
    Bob randomly picks measurement bases and measures incoming qubits.
    """
    num_qubits = len(transmitted_bits)
    bob_bases  = [random.choice(['+', '×']) for _ in range(num_qubits)]
    bob_bits   = []

    for i in range(num_qubits):
        if bob_bases[i] == transmitted_bases[i]:
            # Correct basis: Bob measures the bit accurately
            bob_bits.append(transmitted_bits[i])
        else:
            # Wrong basis: random collapse (quantum measurement disturbance)
            bob_bits.append(random.randint(0, 1))

    return {
        'bob_bases': bob_bases,
        'bob_bits':  bob_bits
    }


def sift_key(alice_bits: list, alice_bases: list,
             bob_bits: list, bob_bases: list) -> dict:
    """
    Basis reconciliation over classical channel.
    Keep only bits where Alice's and Bob's bases match.
    """
    alice_sifted = []
    bob_sifted   = []
    matching_idx = []

    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:
            alice_sifted.append(alice_bits[i])
            bob_sifted.append(bob_bits[i])
            matching_idx.append(i)

    return {
        'alice_sifted': alice_sifted,
        'bob_sifted':   bob_sifted,
        'matching_idx': matching_idx,
        'sift_count':   len(alice_sifted)
    }
