"""
Module 5: Bob Module & Key Sifting

Bob measures received qubits in randomly chosen bases, then compares
with Alice to keep only bits where their bases matched (sifted key).

Description:
    The Bob module implements the receiver side of the BB84 protocol:
    1. Bob randomly selects measurement bases for each received qubit
    2. Bob performs measurements and records results
    3. Bob and Alice publicly compare bases (not the bits)
    4. They keep only the bits where bases matched (sifted key)

BB84 Measurement Rules:
    - If Bob's basis matches Alice's basis → measurement result is accurate
    - If Bob's basis differs from Alice's → result is random (50/50)
    This asymmetry is the core security mechanism of BB84

Sifting:
    After measurement, Alice and Bob publicly compare their basis choices
    over an authenticated classical channel. They discard all bits where
    their bases didn't match. The remaining bits form the "sifted key"
    which both parties should share (unless Eve was eavesdropping).
"""

import random
from typing import Dict, List


def bob_measure(transmitted_bits: List[int], transmitted_bases: List[str]) -> Dict[str, List]:
    """
    Bob randomly picks measurement bases and measures incoming qubits.
    
    Bob doesn't know Alice's bases - he makes his own random choices.
    The measurement outcome depends on whether Bob's basis matches the
    encoding basis of each qubit.
    
    Args:
        transmitted_bits (List[int]): The bits as received (possibly corrupted by Eve)
        transmitted_bases (List[str]): The bases used to encode each bit
        
    Returns:
        Dict[str, List]: Dictionary containing:
            - 'bob_bases': List[str] - Bob's randomly chosen measurement bases
            - 'bob_bits': List[int] - Bob's measurement results
            
    Raises:
        ValueError: If bit and basis lists have different lengths
        
    Note:
        The 'transmitted_bases' parameter represents the bases that were actually
        used to encode each qubit. If Eve was eavesdropping, these are Eve's bases
        (after resend). Otherwise, these are Alice's original bases.
    """
    # Validate input
    if len(transmitted_bits) != len(transmitted_bases):
        raise ValueError("transmitted_bits and transmitted_bases must have equal length")
    
    num_qubits = len(transmitted_bits)
    # Bob makes random basis choices for measurement
    bob_bases: List[str] = [random.choice(['+', '×']) for _ in range(num_qubits)]
    bob_bits: List[int] = []

    # Perform measurement for each qubit
    for i in range(num_qubits):
        if bob_bases[i] == transmitted_bases[i]:
            # Correct basis: Bob measures the bit accurately
            # The quantum state collapses to the correct eigenstate
            bob_bits.append(transmitted_bits[i])
        else:
            # Wrong basis: quantum measurement disturbance
            # The qubit collapses to a random state (50% chance of flip)
            bob_bits.append(random.randint(0, 1))

    return {
        'bob_bases': bob_bases,
        'bob_bits': bob_bits
    }


def sift_key(alice_bits: List[int], alice_bases: List[str],
             bob_bits: List[int], bob_bases: List[str]) -> Dict[str, object]:
    """
    Basis reconciliation over the authenticated classical channel.
    
    Alice and Bob publicly compare their basis choices. They keep only the
    bits where their bases matched. These bits form the "sifted key" which
    should be identical at both ends (assuming no eavesdropping).
    
    This is a critical step: the basis comparison itself must be done over
    an authenticated channel (to prevent Eve from manipulating it), but the
    actual bit values are NOT revealed publicly.
    
    Args:
        alice_bits (List[int]): Alice's original random bits
        alice_bases (List[str]): Alice's original random bases
        bob_bits (List[int]): Bob's measurement results
        bob_bases (List[str]): Bob's measurement bases
        
    Returns:
        Dict[str, object]: Dictionary containing:
            - 'alice_sifted': List[int] - Alice's bits where bases matched
            - 'bob_sifted': List[int] - Bob's bits where bases matched
            - 'matching_idx': List[int] - Indices where bases matched
            - 'sift_count': int - Number of bits kept (sifted key length)
            
    Raises:
        ValueError: If input lists have mismatched lengths
        
    Note:
        For a secure channel, the sifted key should be identical on both sides.
        Any discrepancy indicates eavesdropping or channel noise.
    """
    # Validate input
    if not (len(alice_bits) == len(alice_bases) == len(bob_bits) == len(bob_bases)):
        raise ValueError("All input lists must have equal length")
    
    alice_sifted: List[int] = []
    bob_sifted: List[int] = []
    matching_idx: List[int] = []

    # Compare bases and keep matching bits
    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:
            alice_sifted.append(alice_bits[i])
            bob_sifted.append(bob_bits[i])
            matching_idx.append(i)

    return {
        'alice_sifted': alice_sifted,
        'bob_sifted': bob_sifted,
        'matching_idx': matching_idx,
        'sift_count': len(alice_sifted)
    }
